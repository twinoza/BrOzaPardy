"""
Model Classes for Timer objects
"""
import time

class Timer(object):
    def __init__(self, time):
        self.time = time
        self.end_time = time.time() + time

    def start_timer(self):
        """Restart timer"""
        self.end_time = time.time() + self.time
        return

    @property
    def timed_out(self):
        """Returns True if time is up"""
        return time.time() > self.end_time
