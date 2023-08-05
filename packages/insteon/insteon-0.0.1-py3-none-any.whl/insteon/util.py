from time import time as _time
import queue
import threading
import inspect

# CRC stuff

def calc_simple_crc(data):
    return (~(sum(data)) + 1) & 0xFF

def calc_long_crc(data):
    crc = int(0);
    for loop in xrange(0, len(bytes)):
            b = bytes[loop] & 0xFF
            for bit in xrange(0, 8):
                    fb = b & 0x01
                    fb = fb ^ 0x01 if (crc & 0x8000) else fb
                    fb = fb ^ 0x01 if (crc & 0x4000) else fb
                    fb = fb ^ 0x01 if (crc & 0x1000) else fb
                    fb = fb ^ 0x01 if (crc & 0x0008) else fb
                    crc = ((crc << 1) | fb) & 0xFFFF;
                    b = b >> 1
    return crc

class Channel:
    def __init__(self, filter=None, maxqueue=0):
        self._queue = queue.Queue(maxqueue)

        self._counter = 0 # Number of messages queued
        self._counter_lock = threading.Lock()

        self._filter = filter

    @property
    def has_filter(self):
        return self._filter is not None

    @property
    def active(self):
        return not self._queue.empty()

    @property
    def has_activated(self):
        return self.num_sent > 0

    @property
    def num_sent(self):
        with self._counter_lock:
            return self._counter

    def reset_num_sent(self):
        with self._counter_lock:
            self._counter = 0

    def clear(self):
        with self._queue.mutex:
            self._queue.queue.clear()

    def set_queuesize(self, newsize):
        # oops, just for get about the current
        # elements for now
        self._queue = queue.Queue(newsize)

    def set_filter(self, filter):
        self._filter = filter

    # Will stack another filter ontop of the current one
    def chain_filter(self, filter):
        if self._filter:
            f = self._filter
            def chain(*args):
                return f(*args) and filter(*args)
            self._filter = chain
        else:
            self._filter = filter

    # Waits until there is at least one element in the queue
    # but doesn't take it
    def wait(self, timeout=None):
        with self._queue.not_empty:
            if timeout is None:
                if not self._queue._qsize():
                    self._queue.not_empty.wait()
                return True
            elif timeout > 0:
                endtime = _time() + timeout
                while not self._queue._qsize():
                    remaining = endtime - _time()
                    if remaining <= 0.0:
                        return False
                    self._queue.not_empty.wait(remaining)
                return True
            elif timeout <= 0:
                # Just return whether there
                # is anything in the queue
                return self._queue._qsize()

    def recv(self, timeout=None):
        try:
            if timeout is None:
                return self._queue.get()
            elif timeout > 0:
                return self._queue.get(True, timeout)
            elif timeout <= 0:
                return self._queue.get(False)
        except queue.Empty:
            return None

    def send(self, *args):
        # Push args tuple onto queue
        # if only a single arg, push the first arg
        arg = args
        if len(arg) == 1:
            arg = args[0]
        elif len(arg) == 0:
            arg = None

        try:
            if not self._filter or self._filter(*args):
                with self._counter_lock:
                    self._counter = self._counter + 1
                    self._queue.put(arg)
        except queue.Full:
            return # Drop...

    def __call__(self, *args):
        self.send(*args)

# A custom insteon error type
# that the terminal knows can just be printed out
# without a stack trace
# this should be used for when messages are dropped
# (i.e any unexpected behavior on the insteon network
# or with the modem)
class InsteonError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        self.quiet = True
