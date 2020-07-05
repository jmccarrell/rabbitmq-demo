import sys
from kombu import Connection

with Connection('amqp://user:bitnami@localhost:5672//') as conn:
    with conn.SimpleQueue('simple_queue') as simple_queue:
        while True:
            try:
                msg = simple_queue.get(block=True, timeout=1)
                print(f'Received: {msg.payload}')
                msg.ack()
            except Exception as exc:
                print(f'caught exception: {exc}', file=sys.stderr)
