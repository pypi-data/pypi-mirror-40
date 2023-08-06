from queue import Queue, Empty
import threading
import logging
import time

log = logging.getLogger(__name__)


class Broker:
    qs = {}
    thrs = {}
    work = True

    def send(self, alias, message):
        """send message to queue alias"""
        if not alias in self.qs:
            raise Exception("undefined queue {}".format(alias))
        self.qs[alias].put(message)
        log.debug("new message on {}".format(alias))

    def is_consumer_working(self, consumer_name):
        return self.work

    def _get_message(self, alias, timeout=None):
        if not alias in self.qs:
            raise Exception("undefined queue {}".format(alias))
        try:
            return self.qs[alias].get(timeout=timeout)
        except Empty:
            return None

    def register_consumer(self, target, instances=1):
        """use consumer decorator"""
        self.qs[target.__name__] = Queue()
        self.thrs[target.__name__] = []
        for i in range(0, instances):
            thr = threading.Thread(target=self._consume, args=(target,))
            self.thrs[target.__name__].append(thr)
        [thr.start() for thr in self.thrs[target.__name__]]
        log.info("consumer {} registered".format(target.__name__))

    def stop(self):
        self.work = False

    def is_queue_empty(self, alias):
        return self.qs[alias].empty()

    def loop(self, condition=lambda: True):
        time.sleep(1)
        while condition:
            time.sleep(1)
        self.stop()

    @staticmethod
    def get_local_context():
        return threading.local()

    @staticmethod
    def _consume(f):
        log.info("consumer {} thread {} started".format(f.__name__, threading.get_ident()))
        while broker.is_consumer_working(f.__name__):
            kwargs = broker._get_message(f.__name__, timeout=1)
            if kwargs is None:
                continue
            log.debug("consumer {} thread {} get message".format(f.__name__, threading.get_ident()))
            try:
                f(**kwargs)
            except Exception as ex:
                log.error("consumer {} thread {} exception {}".format(f.__name__, threading.get_ident(), ex))
        log.info("consumer {} thread {} stoped".format(f.__name__, threading.get_ident()))


# default broker
broker = Broker()


def consumer(broker=broker, instances=1):
    """consumer decorator"""

    def wrapper(f):
        broker.register_consumer(f, instances)

    return wrapper
