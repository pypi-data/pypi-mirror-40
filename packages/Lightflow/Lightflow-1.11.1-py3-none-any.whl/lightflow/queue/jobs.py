import celery
from datetime import datetime
from functools import partial

from lightflow.logger import get_logger
from lightflow.models.task_signal import TaskSignal
from lightflow.models.task_context import TaskContext
from lightflow.models.dag_signal import DagSignal
from lightflow.models.datastore import DataStore, DataStoreDocumentSection
from lightflow.models.signal import Server, Client, SignalConnection
from .const import JobType, JobEventName

logger = get_logger(__name__)


@celery.task(bind=True)
def execute_workflow(self, workflow, workflow_id=None):
    """ Celery task (aka job) that runs a workflow on a worker.

    This celery task starts, manages and monitors the dags that make up a workflow.

    Args:
        self (Task): Reference to itself, the celery task object.
        workflow (Workflow): Reference to the workflow object that is being used to
                             start, manage and monitor dags.
        workflow_id (string): If a workflow ID is provided the workflow run will use
                              this ID, if not a new ID will be auto generated.
    """
    start_time = datetime.utcnow()

    logger.info('Running workflow <{}>'.format(workflow.name))
    data_store = DataStore(**self.app.user_options['config'].data_store,
                           auto_connect=True)

    # create a unique workflow id for this run
    if data_store.exists(workflow_id):
        logger.info('Using existing workflow ID: {}'.format(workflow_id))
    else:
        workflow_id = data_store.add(payload={
                                         'name': workflow.name,
                                         'queue': workflow.queue,
                                         'start_time': start_time
                                     })
        logger.info('Created workflow ID: {}'.format(workflow_id))

    # send custom celery event that the workflow has been started
    self.send_event(JobEventName.Started,
                    job_type=JobType.Workflow,
                    name=workflow.name,
                    queue=workflow.queue,
                    time=start_time,
                    workflow_id=workflow_id,
                    duration=None)

    # create server for inter-task messaging
    signal_server = Server(SignalConnection(**self.app.user_options['config'].signal,
                                            auto_connect=True),
                           request_key=workflow_id)

    # store job specific meta information wth the job
    self.update_state(meta={'name': workflow.name,
                            'type': JobType.Workflow,
                            'workflow_id': workflow_id,
                            'queue': workflow.queue,
                            'start_time': start_time,
                            'arguments': workflow.provided_arguments})

    # run the DAGs in the workflow
    workflow.run(config=self.app.user_options['config'],
                 data_store=data_store,
                 signal_server=signal_server,
                 workflow_id=workflow_id)

    end_time = datetime.utcnow()
    duration = (end_time - start_time).total_seconds()

    # update data store with provenance information
    store_doc = data_store.get(workflow_id)
    store_doc.set(key='end_time', value=end_time,
                  section=DataStoreDocumentSection.Meta)
    store_doc.set(key='duration', value=duration,
                  section=DataStoreDocumentSection.Meta)

    # send custom celery event that the workflow has succeeded
    event_name = JobEventName.Succeeded if not workflow.is_stopped \
        else JobEventName.Aborted

    self.send_event(event_name,
                    job_type=JobType.Workflow,
                    name=workflow.name,
                    queue=workflow.queue,
                    time=end_time,
                    workflow_id=workflow_id,
                    duration=duration)

    logger.info('Finished workflow <{}>'.format(workflow.name))


@celery.task(bind=True)
def execute_dag(self, dag, workflow_id, data=None):
    """ Celery task that runs a single dag on a worker.

    This celery task starts, manages and monitors the individual tasks of a dag.

    Args:
        self (Task): Reference to itself, the celery task object.
        dag (Dag): Reference to a Dag object that is being used to start, manage and
                   monitor tasks.
        workflow_id (string): The unique ID of the workflow run that started this dag.
        data (MultiTaskData): An optional MultiTaskData object that is being passed to
                              the first tasks in the dag. This allows the transfer of
                              data from dag to dag.
    """
    start_time = datetime.utcnow()
    logger.info('Running DAG <{}>'.format(dag.name))

    store_doc = DataStore(**self.app.user_options['config'].data_store,
                          auto_connect=True).get(workflow_id)
    store_loc = 'log.{}'.format(dag.name)

    # update data store with provenance information
    store_doc.set(key='{}.start_time'.format(store_loc), value=start_time,
                  section=DataStoreDocumentSection.Meta)

    # send custom celery event that the dag has been started
    self.send_event(JobEventName.Started,
                    job_type=JobType.Dag,
                    name=dag.name,
                    queue=dag.queue,
                    time=start_time,
                    workflow_id=workflow_id,
                    duration=None)

    # store job specific meta information wth the job
    self.update_state(meta={'name': dag.name,
                            'queue': dag.queue,
                            'type': JobType.Dag,
                            'workflow_id': workflow_id})

    # run the tasks in the DAG
    signal = DagSignal(Client(SignalConnection(**self.app.user_options['config'].signal,
                                               auto_connect=True),
                              request_key=workflow_id), dag.name)
    dag.run(config=self.app.user_options['config'],
            workflow_id=workflow_id,
            signal=signal,
            data=data)

    end_time = datetime.utcnow()
    duration = (end_time - start_time).total_seconds()

    # update data store with provenance information
    store_doc.set(key='{}.end_time'.format(store_loc), value=end_time,
                  section=DataStoreDocumentSection.Meta)
    store_doc.set(key='{}.duration'.format(store_loc), value=duration,
                  section=DataStoreDocumentSection.Meta)

    # send custom celery event that the dag has succeeded
    event_name = JobEventName.Succeeded if not signal.is_stopped else JobEventName.Aborted
    self.send_event(event_name,
                    job_type=JobType.Dag,
                    name=dag.name,
                    queue=dag.queue,
                    time=end_time,
                    workflow_id=workflow_id,
                    duration=duration)

    logger.info('Finished DAG <{}>'.format(dag.name))


@celery.task(bind=True)
def execute_task(self, task, workflow_id, data=None):
    """ Celery task that runs a single task on a worker.

    Args:
        self (Task): Reference to itself, the celery task object.
        task (BaseTask): Reference to the task object that performs the work
                         in its run() method.
        workflow_id (string): The unique ID of the workflow run that started this task.
        data (MultiTaskData): An optional MultiTaskData object that contains the data
                              that has been passed down from upstream tasks.
    """
    start_time = datetime.utcnow()

    store_doc = DataStore(**self.app.user_options['config'].data_store,
                          auto_connect=True).get(workflow_id)
    store_loc = 'log.{}.tasks.{}'.format(task.dag_name, task.name)

    def handle_callback(message, event_type, exc=None):
        msg = '{}: {}'.format(message, str(exc)) if exc is not None else message

        # set the logging level
        if event_type == JobEventName.Stopped:
            logger.warning(msg)
        elif event_type == JobEventName.Aborted:
            logger.error(msg)
        else:
            logger.info(msg)

        current_time = datetime.utcnow()

        # store provenance information about a task
        if event_type != JobEventName.Started:
            duration = (current_time - start_time).total_seconds()

            store_doc.set(key='{}.end_time'.format(store_loc),
                          value=current_time,
                          section=DataStoreDocumentSection.Meta)

            store_doc.set(key='{}.duration'.format(store_loc),
                          value=duration,
                          section=DataStoreDocumentSection.Meta)
        else:
            # store provenance information about a task
            store_doc.set(key='{}.start_time'.format(store_loc),
                          value=start_time,
                          section=DataStoreDocumentSection.Meta)

            store_doc.set(key='{}.worker'.format(store_loc),
                          value=self.request.hostname,
                          section=DataStoreDocumentSection.Meta)

            store_doc.set(key='{}.queue'.format(store_loc),
                          value=task.queue,
                          section=DataStoreDocumentSection.Meta)
            duration = None

        # send custom celery event
        self.send_event(event_type,
                        job_type=JobType.Task,
                        name=task.name,
                        queue=task.queue,
                        time=current_time,
                        workflow_id=workflow_id,
                        duration=duration)

    # store job specific meta information wth the job
    self.update_state(meta={'name': task.name,
                            'queue': task.queue,
                            'type': JobType.Task,
                            'workflow_id': workflow_id})

    # send start celery event
    handle_callback('Start task <{}>'.format(task.name), JobEventName.Started)

    # run the task and capture the result
    return task._run(
        data=data,
        store=store_doc,
        signal=TaskSignal(Client(
            SignalConnection(**self.app.user_options['config'].signal, auto_connect=True),
            request_key=workflow_id),
            task.dag_name),
        context=TaskContext(task.name, task.dag_name, task.workflow_name,
                            workflow_id, self.request.hostname),
        success_callback=partial(handle_callback,
                                 message='Complete task <{}>'.format(task.name),
                                 event_type=JobEventName.Succeeded),
        stop_callback=partial(handle_callback,
                              message='Stop task <{}>'.format(task.name),
                              event_type=JobEventName.Stopped),
        abort_callback=partial(handle_callback,
                               message='Abort workflow <{}> by task <{}>'.format(
                                   task.workflow_name, task.name),
                               event_type=JobEventName.Aborted))
