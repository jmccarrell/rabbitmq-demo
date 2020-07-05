import sys
import datetime

from kombu import Connection
from connection import make_connection_url


# print(f'connection string: {make_connection_url()}', file=sys.stderr)
with Connection(make_connection_url()) as conn:
    with conn.SimpleQueue('simple_queue') as simple_queue:
        msg = f'hello Jeff; sent at {datetime.datetime.now()}'
        simple_queue.put(msg)
        print(f'Sent: {msg}')
