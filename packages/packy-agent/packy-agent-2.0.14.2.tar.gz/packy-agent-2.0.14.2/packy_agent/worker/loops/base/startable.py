import logging
import time
from abc import ABC

from packy_agent.worker.loops.base.loop import Loop
from packy_agent.utils.gevent import CustomGreenlet


TOTAL_DURATION_MAX_SECONDS = 0.1
SINGLE_DURATION_MAX_SECONDS = 0.01

logger = logging.getLogger(__name__)


class StartableLoop(Loop, ABC):

    loop_type = 'startable'

    def __init__(self, is_safe_iteration=True, is_logged_iteration=True):
        super().__init__(is_safe_iteration=is_safe_iteration,
                         is_logged_iteration=is_logged_iteration)
        self.greenlet = None
        self.is_started = False

    def get_greenlet(self):
        return self.greenlet

    def start(self):
        if self.is_started:
            return

        self.greenlet = CustomGreenlet(self.loop)
        self.greenlet.start()
        self.is_started = True

    def join(self):
        self.greenlet.join()

    def iteration_wrapper(self):
        greenlet = self.get_greenlet()
        if greenlet:
            greenlet.clear_switch_log()

        start = time.time()
        return_value = super().iteration_wrapper()
        finish = time.time()

        if greenlet:
            durations = greenlet.get_switch_log_durations()
            total_duration = sum(durations)
            if durations:
                longest_duration = max(durations)
                if (total_duration >= TOTAL_DURATION_MAX_SECONDS or
                        longest_duration >= SINGLE_DURATION_MAX_SECONDS):
                    logger_method = logger.warning
                else:
                    logger_method = logger.debug

                logger_method('SPENT %.6gs in greenlet (%.6gs in real time) during %s '
                              'iteration (%s switches), longest switch is %.6gs',
                              total_duration, finish - start, self.description,
                              len(durations), longest_duration)

        return return_value
