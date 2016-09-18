from .base import Resource


class KalaStats(Resource):
    """Stats resource
    :param int active_jobs: number of kala active jobs
    :param int disabled_jobs: number of kala disabled jobs
    :param int jobs: number of kala jobs
    :param int error_count: number of job errors
    :param int success_count: number of successful runs
    :param string next_run_at: date of the next job run
    :param string last_attempted_run: date of last run attemption
    :param string created: job creation date
    """

    def __init__(self, active_jobs=None, disabled_jobs=None, jobs=None,
                 error_count=None, success_count=None, next_run_at=None,
                 last_attempted_run=None, created=None):
        self.active_jobs = active_jobs
        self.disabled_jobs = disabled_jobs
        self.jobs = jobs
        self.error_count = error_count
        self.success_count = success_count
        self.next_run_at = next_run_at
        self.last_attempted_run = last_attempted_run
        self.created = created
