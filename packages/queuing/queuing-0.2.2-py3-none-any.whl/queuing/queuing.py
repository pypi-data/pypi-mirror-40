from queue import Queue
import _thread 

class Broker:
    qs = {}
    thrs = {}
    
    def __init__(self):
        pass
    
    def send(self, alias, message):
        if not alias in self.qs:
            raise Exception("undefined queue {}".format(alias))
        self.qs[alias].put(message)

    def is_consumer_working(self, consumer_name):
        return True
        
    def get_message(self, alias):
        if not alias in self.qs:
            raise Exception("undefined queue {}".format(alias))
        return self.qs[alias].get()
        
    def register_consumer(self, target, instances=1):
        self.qs[target.__name__] = Queue()
        self.thrs[target.__name__]=[_thread.start_new(self._consume, (target,)) for i in range(0,instances)]
        
    def _consume(self, f):
        while broker.is_consumer_working(f.__name__):
            res = broker.get_message(f.__name__)
            f(res)

broker = Broker()

def consumer(broker=broker, instances=1):
    def wrapper(f):
        broker.register_consumer(f, instances)
    return wrapper
            
@consumer()
def w1(no):
    print("w1 {}".format(no))
    broker.send('w2', no)

@consumer()
def w2(no):
    print("w2 {}".format(no))
    broker.send('w3', no)
    broker.send('w3', no)

@consumer(instances=3)
def w3(no):
    print("w3 {}".format(no))

def main():
    [broker.send('w1', i) for i in range(0, 100)]

if __name__ == "__main__":
    main()

