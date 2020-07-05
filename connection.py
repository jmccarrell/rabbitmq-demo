from os import environ

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


