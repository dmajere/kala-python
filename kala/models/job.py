from .base import Resource


class Job(Resource):

    """Docstring for Job.
    :param string name: Job name
    :param string id: Job Id
    :param string command: Command to run
    :param string owner: Email of the owner of this job
    :param bool disabled: Is this job disabled?
    :param list[string] dependent_jobs: Jobs that are dependent upon \
this one will be run after this job runs.
    :param list[string] parent_jobs: List of ids of jobs that this job \
is dependent upon.
    :param string schedule:  ISO 8601 String
    :param int retries: Number of times to retry on failed attempt for each run
    :param string epsilon: Duration in which it is safe to retry the Job
    :param string next_run_at: Date of the next run
    :param metadata: Meta data about successful and failed runs.
    :type metadata: :class:kala.models.JobMetadata
    :param stats: Collection of Job Stats
    :type stats: :class:kala.models.JobStats
    :param bool is_done: Says if a job has been executed right numbers \
of time and should not been executed again in the future
    """

    def __init__(self, name=None, id=None, command=None,
                 owner=None, disabled=False, dependent_jobs=None,
                 parent_jobs=None, schedule=None, retries=None,
                 epsilon=None, next_run_at=None, metadata=None,
                 stats=None, is_done=None):

        self.name = name
        self.id = id
        self.command = command
        self.owner = owner
        self.disabled = disabled
        self.dependent_jobs = dependent_jobs
        self.parent_jobs = parent_jobs
        self.schedule = schedule
        self.retries = retries
        self.epsilon = epsilon
        self.next_run_at = next_run_at
        if metadata:
            self.metadata = (
                metadata if isinstance(metadata, JobMetadata)
                else JobMetadata.from_json(metadata))
        self.stats = [
            st if isinstance(st, JobStat) else JobStat.from_json(st)
            for st in (stats or [])]


class JobMetadata(Resource):

    """Docstring for JobMetadata.

    :param int success_count: Number of successful runs
    :param string last_success: Last successful run date
    :param int error_count: Number of failed runs
    :param string last_error: Last failed run date
    :param string last_attempted_run: Last attempted run date
    """

    def __init__(self, success_count=None, last_success=None,
                 error_count=None, last_error=None,
                 last_attempted_run=None):
        self.success_count = success_count
        self.last_success = last_success
        self.error_count = error_count
        self.last_error = last_error
        self.last_attempted_run = last_attempted_run


class JobStat(Resource):

    """Docstring for JobStat.
    :param string job_id:  Job Id
    :param string ran_at: Job runned at
    :param int number_of_retries: Number of job retries
    :param bool success: Is job succesful
    :param int execution_duration: Job run duration
    """

    def __init__(self, job_id=None, ran_at=None,
                 number_of_retries=None, success=None,
                 execution_duration=None):
        self.job_id = job_id
        self.ran_at = ran_at
        self.number_of_retries = number_of_retries
        self.success = success
        self.execution_duration = execution_duration
