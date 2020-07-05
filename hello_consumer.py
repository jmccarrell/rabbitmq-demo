import sys

from kombu import Connection
from connection import make_connection_url


# print(f'connection string: {make_connection_url()}', file=sys.stderr)
with Connection(make_connection_url()) as conn:
    with conn.SimpleQueue('simple_queue') as simple_queue:
        while True:
            try:
                msg = simple_queue.get(block=True, timeout=1)
                print(f'Received: {msg.payload}')
                msg.ack()
            except Exception as exc:
                print(f'caught exception: {exc}', file=sys.stderr)
