import threading
import traceback
import queue
import copy
import weakref

import time

from . import message
from .. import util as util

import logbook

logger = logbook.Logger(__name__)

class WriteRequest:
    def __init__(self, msg, priority=1, prewrite_quiet_time=0, postwrite_quiet_time=0,
            write_channel=None, first_reply_channel=None,
            ack_reply_channel=None, custom_channels=[], weakref_customs=True):
        self.msg = msg
        self.priority = priority

        self.prewrite_quiet_time = prewrite_quiet_time
        self.postwrite_quiet_time = postwrite_quiet_time

        self.write_channel = write_channel 

        self.first_reply_channel = first_reply_channel

        ack_msg_name = msg.type + 'Reply'

        # We must have this channel to know if we have received an ack!
        self.ack_reply_channel = ack_reply_channel if ack_reply_channel else \
                util.Channel(lambda x: x.type == ack_msg_name, 1)

        if not self.ack_reply_channel.has_filter or self.ack_reply_channel.has_activated:
            # No filter or if we are reusing a channel
            self.ack_reply_channel.reset_num_sent()
            self.ack_reply_channel.set_filter(lambda x: x.type == ack_msg_name)

        self.custom_channels = custom_channels # Will be added with write() call
        self.weakref_customs = weakref_customs

    def __gt__(self, other):
        return self.priority > other.priority
    def __lt__(self, other):
        return self.priority < other.priority
    def __ge__(self, other):
        return self.priority >= other.priority
    def __le__(self, other):
        return self.priority <= other.priority
    def __eq__(self, other):
        return self.priority == other.priority
    def __nq__(self, other):
        return self.priority != other.priority

# Takes a connection object that has read(), write(), flush(), and close() methods
class Port:
    def __init__(self, conn=None, definitions={}):
        self.defs = definitions

        # Connection and threads
        self._conn = None
        self._reader = None
        self._writer = None

        # A queue containing write requests
        self._write_queue = queue.PriorityQueue()

        # Setup the listeners
        self._read_listeners = []
        self._read_listeners_lock = threading.RLock()

        self._write_listeners = []
        self._write_listeners_lock = threading.RLock()

        # Setup the watchers, for optional use by the user
        # to print out to stdout the traffic through the port
        self._read_watcher = lambda x: print(str(x))
        self._write_watcher = lambda x: print(str(x))

        if conn:
            self.attach(conn)

    def __del__(self):
        self.detach()

    def attach(self, conn):
        if self._conn:
            self.detach()

        # Start threads
        self._conn = conn
        self._reader = threading.Thread(target=self._read_thread, daemon=True)
        self._writer = threading.Thread(target=self._write_thread, daemon=True)

        # Trigger for a thread to stop
        self._reader.stop = self.close
        self._writer.stop = self.close

        self._reader.start()
        self._writer.start()

    def detach(self):
        if self._reader:
            r = self._reader
            self._reader = None
            r.join()
        if self._writer:
            w = self._writer
            self._writer = None
            w.join()

        self._conn = None

    def close(self): # Detaches and closes the connection
        if self._conn:
            conn = self._conn
            self.detach()
            conn.close()

    def notify_on_read(self, handler):
        if not handler:
            return
        with self._read_listeners_lock:
            self._read_listeners.append(handler)

    def unregister_on_read(self, handler):
        if not handler:
            return
        with self._read_listeners_lock:
            if handler in self._read_listeners:
                self._read_listeners.remove(handler)

    def notify_on_write(self, handler):
        if not handler:
            return
        with self._write_listeners_lock:
            self._write_listeners.append(handler)

    def unregister_on_write(self, handler):
        if not handler:
            return
        with self._write_listeners_lock:
            if handler in self._write_listeners:
                self._write_listeners.remove(handler)

    # Utility debug functions.....

    def start_watching(self):
        self.notify_on_read(self._read_watcher)
        self.notify_on_write(self._write_watcher)
    
    def stop_watching(self):
        self.unregister_on_read(self._read_watcher)
        self.unregister_on_write(self._write_watcher)

    # Now the actual IO logic
    # added as weak references, so they won't stay
    # around if the channel goes out of scope by the original caller
    def write(self, msg, priority=1, prewrite_quiet_time=0, postwrite_quiet_time = 0,
            write_channel=None, first_reply_channel=None,
            ack_reply_channel=None, custom_channels=[], weakref_customs=True):

        self.write_request( WriteRequest(msg, priority,
            prewrite_quiet_time, postwrite_quiet_time,
            write_channel, first_reply_channel,
            ack_reply_channel, custom_channels, weakref_customs) )

    def write_request(self, request):
        self._write_queue.put(request)

    def _read_thread(self):
        decoder = message.MsgDecoder(self.defs)
        buf = bytes()
        while self._reader:
            try:
                buf = self._conn.read(1) # Read a byte
                # Feed into decoder
                msg = decoder.decode(buf)
                if not msg:
                    continue
            except TypeError as te: # Gets thrown on close() called during read() sometimes
                continue
            except Exception as e:
                print('Error reading!')
                print(traceback.format_exc())
                continue
            
            # Notify listeners
            with self._read_listeners_lock:
                listeners = list(self._read_listeners)
                for lr in listeners:
                    if isinstance(lr, weakref.ref):
                        l = lr()
                        if not l:
                            self._read_listeners.remove(lr)
                            continue
                    else:
                        l = lr
                    l(msg)

    def _write_thread(self):
        while self._writer:
            try:
                request = self._write_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            # Wait the pre-write quiet time we want
            # during this time all is quiet
            if request.prewrite_quiet_time > 0:
                time.sleep(request.prewrite_quiet_time)

            msg = request.msg

            # Callback channels to notify on write/read:
            write_channel = request.write_channel
            first_reply_channel = request.first_reply_channel
            ack_reply_channel = request.ack_reply_channel

            if write_channel:
                write_channel.set_queuesize(1)
                write_channel.set_filter(None)

            if first_reply_channel:
                first_reply_channel.set_filter(None)

            # Our channels for writer control
            any_reply_channel = util.Channel() # For writer control
            any_reply_channel.set_filter(None) # Let everything in

            nack_reply_channel = util.Channel() # For writer control
            nack_reply_channel.set_filter(lambda msg: msg.type == 'PureNACK')

            # Get the listener lock so we don't miss anything
            # while we write
            with self._read_listeners_lock:
                # Add the channels
                self.notify_on_read(any_reply_channel)
                self.notify_on_read(nack_reply_channel)

                self.notify_on_read(first_reply_channel)
                self.notify_on_read(ack_reply_channel)

                self.notify_on_write(write_channel)

                # Will be removed by hand by the person who
                # queued the write if weakref_customs is False
                # otherwise will be automatically removed
                for channel in request.custom_channels:
                    if request.weakref_customs:
                        self.notify_on_read(weakref.ref(channel))
                    else:
                        self.notify_on_read(channel)

                for i in range(5): # Maximum of 5 resends...

                    # Now we do the actual writing
                    try: 
                        data = msg.bytes
                        self._conn.write(data)
                        self._conn.flush()
                    except Exception as e:
                        # TODO: Make logging
                        print('Error writing message!')
                        print(traceback.format_exc())
                        break # Move on to the next message

                    # Notify the listeners of the write
                    with self._write_listeners_lock:
                        listeners = list(self._write_listeners)
                        for lr in listeners:
                            if isinstance(lr, weakref.ref):
                                l = lr()
                                if not l:
                                    self._write_listeners.remove(lr)
                                    continue
                            else:
                                l = lr
                            l(msg)

                    # Remove the write channel the first time we write
                    if i == 0:
                        self.unregister_on_write(write_channel)

                    # Now we see what comes back by disabling the listener lock
                    self._read_listeners_lock.release()

                    resend = False
                    for mi in range(6): # Look at the next 6 messages or 0.6 second, max
                        if any_reply_channel.wait(0.1): # Wait 100ms for something to arrive
                            # Check if what came was an ack or nack
                            if ack_reply_channel.has_activated:
                                # Woo, we are done, no resend
                                break
                            elif nack_reply_channel.has_activated:
                                # Resend on a nack
                                any_reply_channel.clear()
                                nack_reply_channel.clear()
                                resend = True
                                break
                            else:
                                # Other message type...wait again
                                any_reply_channel.clear()

                    if not ack_reply_channel.has_activated and not resend:
                        # Resend due to no ack!
                        any_reply_channel.clear()
                        nack_reply_channel.clear()
                        resend = True

                    # Re-acquire so the with block doesn't get confused
                    self._read_listeners_lock.acquire() 

                    if not resend:
                        break

                # Remove the listeners
                self.unregister_on_read(first_reply_channel)
                self.unregister_on_read(ack_reply_channel)
                self.unregister_on_read(any_reply_channel)
                self.unregister_on_read(nack_reply_channel)

                # In case this hasn't happened
                self.unregister_on_write(write_channel)
            # Now outside of the lock,
            # post-write quiet time
            if request.postwrite_quiet_time > 0:
                time.sleep(request.postwrite_quiet_time)
