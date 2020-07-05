import sys
import time

from kombu import Connection
from connection import make_connection_url
from token_bucket import TokenBucket

consume_rate = 6  # per second
rate_limit = TokenBucket(consume_rate, consume_rate * 10)

# print(f'connection string: {make_connection_url()}', file=sys.stderr)
with Connection(make_connection_url()) as conn:
    with conn.SimpleQueue('simple_queue') as simple_queue:
        while True:
            try:
                if rate_limit.can_consume(1):
                    msg = simple_queue.get(block=True, timeout=1)
                    print(f'Received: {msg.payload}')
                    msg.ack()
                else:
                    sleep_for = rate_limit.expected_time()
                    print(f'consume_rate: {consume_rate}; sleep({sleep_for})')
                    time.sleep(rate_limit.expected_time())
            except Exception as exc:
                print(f'caught exception: {exc}', file=sys.stderr)
