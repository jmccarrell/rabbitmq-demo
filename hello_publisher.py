import datetime

from kombu import Connection

with Connection('amqp://user:bitnami@localhost:5672') as conn:
    with conn.SimpleQueue('simple_queue') as simple_queue:
        msg = f'hello Jeff; sent at {datetime.datetime.now()}'
        simple_queue.put(msg)
        print(f'Sent: {msg}')
