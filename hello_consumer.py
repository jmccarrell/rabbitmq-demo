import sys
from os import environ
from kombu import Connection

required_environment_vars = tuple(('RABBITMQ_USERNAME',
                                   'RABBITMQ_PASSWORD',
                                   'RABBITMQ_NODE_PORT_NUMBER',
                                   'RABBITMQ_VHOST',))


def make_connection_url() -> str:
    # check for required runtime parameters
    missing_env_vars = []
    for e in required_environment_vars:
        if environ.get(e) is None:
            missing_env_vars.append(e)
    if len(missing_env_vars) > 0:
        raise RuntimeError(f'expected environment vars for config: {missing_env_vars}')

    return ''.join((f"amqp://{environ['RABBITMQ_USERNAME']}:{environ['RABBITMQ_PASSWORD']}",
                    f"@localhost:{environ['RABBITMQ_NODE_PORT_NUMBER']}/{environ['RABBITMQ_VHOST']}"))


with Connection(make_connection_url()) as conn:
    with conn.SimpleQueue('simple_queue') as simple_queue:
        while True:
            try:
                msg = simple_queue.get(block=True, timeout=1)
                print(f'Received: {msg.payload}')
                msg.ack()
            except Exception as exc:
                print(f'caught exception: {exc}', file=sys.stderr)
