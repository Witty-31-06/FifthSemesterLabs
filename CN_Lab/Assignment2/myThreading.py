import threading
import collections

class myThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name,
                         daemon=daemon)
        self._args = args
        self._kwargs = kwargs or {}
        self.ptr1 = 0
        self.pending_frames = collections.OrderedDict()

    def run(self):
        if self._target:
            self.ptr1, self.pending_frames = self._target(*self._args,
                                                          **self._kwargs)

    def join(self, timeout=None):
        super().join(timeout)  # Wait for the thread to finish
        return self.ptr1, self.pending_frames
