import schedule as baseSchedule
import datetime
import random
import threading
import time
from chatqhelper import debug


logger = debug.logger(__name__)


class UTCScheduler(baseSchedule.Scheduler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._thread = None
        self._thread_terminate = True

    @property
    def idle_seconds(self):
        return (self.next_run - datetime.datetime.utcnow()).total_seconds()

    def schedule(self, setting, task):
        every = setting['every']
        if isinstance(every, str):
            job = getattr(self.every(), every)
        elif len(every) == 2:
            interval, time_unit = every
            job = getattr(self.every(interval), time_unit)
        else:
            from_interval, to_interval, time_unit = every
            job = getattr(self.every(from_interval).to(to_interval), time_unit)

        if 'at' in setting:
            job.at(setting['at'])

        job.do(task)
        return job

    def every(self, interval=1):
        job = UTCJob(interval, self)
        return job

    def loop_start(self, interval=1):
        if self._thread is not None:
            self.loop_stop()

        self._thread_terminate = False
        self._thread_interval = interval
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def loop_stop(self):
        if self._thread is None:
            return

        self._thread_terminate = True
        if threading.current_thread() != self._thread:
            self._thread.join()
            self._thread = None

    def _loop(self):
        while not self._thread_terminate:
            time.sleep(self._thread_interval)
            self.run_pending()

    def run_pending(self):
        runnable_jobs = (job for job in self.jobs if job.should_run)
        for job in sorted(runnable_jobs):
            try:
                self._run_job(job)
            except Exception as e:
                logger.error('exception while running scheduled jobs -- ' + str(e))
                debug.log_traceback(logger)


class UTCJob(baseSchedule.Job):
    @property
    def should_run(self):
        return datetime.datetime.utcnow() >= self.next_run

    def _schedule_next_run(self):
        assert self.unit in ('seconds', 'minutes', 'hours', 'days', 'weeks')
        if self.latest is not None:
            assert self.latest >= self.interval
            interval = random.randint(self.interval, self.latest)
        else:
            interval = self.interval

        self.period = datetime.timedelta(**{self.unit: interval})
        self.next_run = datetime.datetime.utcnow() + self.period
        if self.start_day is not None:
            assert self.unit == 'weeks'
            weekdays = (
                'monday',
                'tuesday',
                'wednesday',
                'thursday',
                'friday',
                'saturday',
                'sunday'
            )

            assert self.start_day in weekdays
            weekday = weekdays.index(self.start_day)
            days_ahead = weekday - self.next_run.weekday()
            if days_ahead <= 0:
                days_ahead += 7

            self.next_run += datetime.timedelta(days_ahead) - self.period

        if self.at_time is not None:
            assert self.unit in ('days', 'hours') or self.start_day is not None
            kwargs = {
                'minute': self.at_time.minute,
                'second': self.at_time.second,
                'microsecond': 0
            }

            if self.unit == 'days' or self.start_day is not None:
                kwargs['hour'] = self.at_time.hour

            self.next_run = self.next_run.replace(**kwargs)
            if not self.last_run:
                now = datetime.datetime.utcnow()
                if (self.unit == 'days' and self.at_time > now.time() and self.interval == 1):
                    self.next_run = self.next_run - datetime.timedelta(days=1)
                elif self.unit == 'hours' and self.at_time.minute > now.minute:
                    self.next_run = self.next_run - datetime.timedelta(hours=1)

        if self.start_day is not None and self.at_time is not None:
            if (self.next_run - datetime.datetime.utcnow()).days >= 7:
                self.next_run -= self.period

    def cancel(self):
        self.scheduler.cancel_job(self)

    def run(self):
        ret = None
        try:
            ret = self.job_func()
        except Exception as e:
            logger.error('exception while execute job function -- ' + str(e))
            debug.log_traceback(logger)

        self.last_run = datetime.datetime.utcnow()
        self._schedule_next_run()
        return ret


default_scheduler = UTCScheduler()


def every(interval=1):
    return default_scheduler.every(interval)


def tick():
    default_scheduler.run_pending()


def loop_start(interval=1):
    default_scheduler.loop_start(interval)


def loop_stop():
    default_scheduler.loop_stop()


def clear(tag=None):
    default_scheduler.clear(tag)


def next_run():
    return default_scheduler.next_run


def idle_seconds():
    return default_scheduler.idle_seconds


def schedule(setting, task):
    return default_scheduler.schedule(setting, task)
