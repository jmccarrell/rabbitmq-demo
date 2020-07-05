import sys
import time
import datetime

from kombu import Connection
from connection import make_connection_url
from token_bucket import TokenBucket

produce_rate = 5  # per second
rate_limit = TokenBucket(produce_rate, produce_rate * 10)

# print(f'connection string: {make_connection_url()}', file=sys.stderr)
with Connection(make_connection_url()) as conn:
    with conn.SimpleQueue('simple_queue') as simple_queue:
        while True:
            try:
                if rate_limit.can_consume(1):
                    msg = f'hello Jeff at rate {produce_rate}/second; sent at {datetime.datetime.now()}'
                    simple_queue.put(msg)
                    print(f'Sent: {msg}')
                else:
                    # sleep_for = rate_limit.expected_time()
                    # print(f'sleep({sleep_for})')
                    time.sleep(rate_limit.expected_time())
            except Exception as exc:
                print(f'caught exception: {exc}', file=sys.stderr)
