# queuing
Multithreating producent-consumer solution

Example
```python
import queuing
import time
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)5s] %(name)s %(message)s')


@queuing.consumer(instances=5)
def m1(no):
    time.sleep(1)
    print("m1 {}".format(no))
    queuing.broker.send('m2', {
        'no': no,
        'sqno': no * no,
    })
    [queuing.broker.send('m3', {
        'no': no,
    }) for i in range(0, 10)]


@queuing.consumer(instances=2)
def m2(no, sqno):
    time.sleep(2)
    print("m2 {} {}".format(no, sqno))


@queuing.consumer(instances=1)
def m3(no):
    print("m3 {}".format(no))


if __name__ == '__main__':
    for i in range(0, 10):
        queuing.broker.send('m1', {
            'no': i
        })

    queuing.broker.loop()

```