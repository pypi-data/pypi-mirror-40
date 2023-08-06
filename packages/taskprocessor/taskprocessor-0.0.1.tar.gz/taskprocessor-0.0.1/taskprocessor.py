# -*- coding: utf-8 -*-

import os
import sys
import math
import inspect
import traceback
import pickle

import numpy as np
import pika
import dill

from collections import OrderedDict
from uuid import uuid4
from contextlib import contextmanager
from multiprocessing import Process
from multiprocessing.pool import RemoteTraceback


TASK_CACHE_SIZE = 1000
task_cache = OrderedDict()


@contextmanager
def create_connection(broker, timeout=1):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=broker, socket_timeout=timeout))
    try:
        yield connection
    finally:
        connection.close()


@contextmanager
def create_channel(connection):
    channel = connection.channel()
    try:
        yield channel
    finally:
        channel.cancel()
        channel.close()


def run_worker(broker='localhost'):
    with create_connection(broker=broker) as conn, create_channel(conn) as channel:
        try:
            channel.tx_select()
            channel.exchange_declare(exchange='task_exchange', durable=True)
            channel.queue_declare(queue='task_queue', durable=True)
            channel.queue_bind(queue='task_queue',
                               exchange='task_exchange',
                               routing_key='tasks')

            for method_frame, properties, body in channel.consume('task_queue'):
                task_id = None
                try:
                    task_id, task_bytes, args, kwargs = pickle.loads(body)
                    assert isinstance(task_id, str)
                    assert isinstance(task_bytes, bytes)

                    # Check if task still required
                    try:
                        with create_channel(conn) as temp_channel:
                            temp_channel.queue_declare(queue=task_id, passive=True)
                    except pika.exceptions.ChannelClosed:
                        continue

                    if task_bytes in task_cache:
                        task = task_cache[task_bytes]
                    else:
                        task = dill.loads(task_bytes)
                        if inspect.isclass(task):
                            task = task()
                        task_cache[task_bytes] = task
                        if len(task_cache) > TASK_CACHE_SIZE:
                            task_cache.popitem()

                    result = task(*args, **kwargs)
                    result_body = pickle.dumps((result, None))
                    channel.basic_publish(body=result_body,
                                          exchange='task_exchange',
                                          routing_key=task_id)
                except Exception as e:
                    tb = ''.join(traceback.format_exception(*sys.exc_info()))
                    error_body = pickle.dumps((None, (e, tb)))
                    channel.basic_publish(body=error_body,
                                          exchange='task_exchange',
                                          routing_key=task_id)
                channel.basic_ack(method_frame.delivery_tag)
                channel.tx_commit()
        except Exception as e:
            print(e)


def run_worker_process(name, broker='localhost'):
    print('Worker %s started' % name)
    while True:
        try:
            run_worker(broker=broker)
        except Exception as e:
            print(e)


def run_main():
    for i in range(int(os.environ['CONCURRENCY'])):
        Process(target=run_worker_process, args=(i, os.environ['BROKER'])).start()


class BatchProcessor:
    def __init__(self, dataset, task, broker='localhost', batch_size=1, drop_last=False):
        self.dataset = dataset
        self.task = task
        self.broker = broker
        self.batch_size = batch_size
        self.drop_last = drop_last

    def __iter__(self):
        task_id = str(uuid4())
        task_bytes = dill.dumps(self.task)

        n = len(self.dataset)
        if self.drop_last:
            batch_total = math.floor(n / self.batch_size)
        else:
            batch_total = math.ceil(n / self.batch_size)

        with create_connection(broker=self.broker) as conn, create_channel(conn) as channel:
            def enqueue_task():
                idxs = np.random.permutation(n)
                for batch in range(batch_total):
                    batch_idxs = idxs[batch * self.batch_size:(batch + 1) * self.batch_size]
                    data = self.dataset[batch_idxs]
                    task_body = pickle.dumps((task_id, task_bytes, (data,), {}))
                    channel.basic_publish(exchange='task_exchange',
                                          routing_key='tasks',
                                          body=task_body)
                    yield True
                while True:
                    yield False

            channel.exchange_declare(exchange='task_exchange', durable=True)
            channel.queue_declare(queue=task_id, durable=True, auto_delete=True)
            channel.queue_bind(queue=task_id,
                               exchange='task_exchange',
                               routing_key=task_id)

            # Prefetch tasks
            do_enqueue = enqueue_task()
            for i in range(3):
                next(do_enqueue)

            for i, (method_frame, properties, body) in enumerate(
                    channel.consume(task_id)):
                result, error = pickle.loads(body)
                channel.basic_ack(method_frame.delivery_tag)
                if error:
                    exception, tb = error
                    exception.__cause__ = RemoteTraceback(tb)
                    raise exception
                try:
                    if not next(do_enqueue) and i + 1 >= batch_total:
                        break
                finally:
                    yield result


if __name__ == '__main__':
    run_main()
