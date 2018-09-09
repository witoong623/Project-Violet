from .matchdb import match_fetch
from django_cron import CronJobBase, Schedule

class MatchFetchCron(CronJobBase):
    RUN_AT_TIMES = ['6:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'website.match_fetch_cron'

    def do(self):
        match_fetch.fetch_and_update_match()