import asyncio
import asynqp


async def send_message_to_exchange(rabbitmq_config: dict, queue_config: dict, message: dict) -> None:
    """
    Send Messages to rabbit mq exchange. Don't use directly.
    :param rabbitmq_config: dict config for rabbitmq instance config: {'host': '', 'port': '', 'username': '',
     'password': ''}
    :param queue_config: dict config of consumer queues: {'exchange': '', 'queues': [], 'routing_key': '',
     'exchange_type': '', 'error_messaging': dict}
    :param message: dict object to be sent
    :return: None
    """
    connection, channel = None, None
    try:
        # connect to the RabbitMQ broker
        connection = await asynqp.connect(rabbitmq_config['host'], rabbitmq_config['port'],
                                          rabbitmq_config['username'], rabbitmq_config['password'])

        # Open a communications channel
        channel = await connection.open_channel()

        # Create an exchange and QUEUE on the broker
        amqp_exchange = await channel.declare_exchange(queue_config['exchange'], queue_config['exchange_type'])
        for queue in queue_config['queues']:
            amqp_queue = await channel.declare_queue(queue)
            await amqp_queue.bind(amqp_exchange, queue_config['routing_key'])

        # If you pass in a dict it will be automatically converted to JSON
        msg = asynqp.Message(message, content_type="application/json")

        amqp_exchange.publish(msg, queue_config['routing_key'])
        print("Published message: {msg} to {exchange}-{routing_key}".
              format(msg=str(message), exchange=queue_config['exchange'], routing_key=queue_config['routing_key']))
    except asynqp.AMQPError:
        print("Unable to publish message to exchange: {exchange} and routing key: {routing_key}".
              format(exchange=queue_config['exchange'], routing_key=queue_config['routing_key']))
        if 'error_messaging' in queue_config.keys():
            error_message = dict(message=message, exchange=queue_config['exchange'], queues=queue_config['queues'],
                                 routing_key=queue_config['routing_key'], exchange_type=queue_config['exchange_type'])
            await send_request_to_error_queue(rabbitmq_config, queue_config['error_messaging'], error_message)
    except asyncio.CancelledError:
        print("Asyncio error : cancelled routine")
    finally:
        if channel is not None:
            await channel.close()
        if connection is not None:
            await connection.close()
        print("Queue channel and connection closed by producer for msg-{msg}".format(msg=message))


async def send_bulk_messages_to_exchange(rabbitmq_config: dict, queue_config: dict, messages: list) -> None:
    """
    Send Messages to rabbit mq exchange. Don't use directly.
    :param rabbitmq_config: dict config for rabbitmq instance config: {'host': '', 'port': '', 'username': '',
     'password': ''}
    :param queue_config: dict config of consumer queues: {'exchange': '', 'queues': [], 'routing_key': '',
     'exchange_type': '', 'error_messaging': dict}
    :param messages: list of dict object(messages) to be sent
    :return: None
    """
    connection, channel = None, None
    try:
        # connect to the RabbitMQ broker
        connection = await asynqp.connect(rabbitmq_config['host'], rabbitmq_config['port'],
                                          rabbitmq_config['username'], rabbitmq_config['password'])

        # Open a communications channel
        channel = await connection.open_channel()

        # Create an exchange and QUEUE on the broker
        amqp_exchange = await channel.declare_exchange(queue_config['exchange'], queue_config['exchange_type'])
        for queue in queue_config['queues']:
            amqp_queue = await channel.declare_queue(queue)
            await amqp_queue.bind(amqp_exchange, queue_config['routing_key'])

        for message in messages:
            # If you pass in a dict it will be automatically converted to JSON
            msg = asynqp.Message(message, content_type="application/json")
            amqp_exchange.publish(msg, queue_config['routing_key'])

        print("Published bulk messages to {exchange}-{routing_key}".
              format(exchange=queue_config['exchange'], routing_key=queue_config['routing_key']))
    except asynqp.AMQPError:
        print("Unable to publish bulk messages to exchange: {exchange} with routing key: {routing_key}".
              format(exchange=queue_config['exchange'], routing_key=queue_config['routing_key']))
        if 'error_messaging' in queue_config.keys():
            error_message = dict(messages=messages, exchange=queue_config['exchange'], queues=queue_config['queues'],
                                 routing_key=queue_config['routing_key'], exchange_type=queue_config['exchange_type'])
            await send_request_to_error_queue(rabbitmq_config, queue_config['error_messaging'], error_message)
    except asyncio.CancelledError:
        print("Asyncio error : cancelled routine")
    finally:
        if channel is not None:
            await channel.close()
        if connection is not None:
            await connection.close()
        print("Queue channel and connection closed")


def send_message(rabbitmq_config: dict, queue_config: dict, message: dict) -> None:
    """
    Send a single message to rabbit mq queues
    :param rabbitmq_config: dict config for rabbitmq instance config: {'host': , 'port': , 'username': , 'password': }
    :param message: dict object(message) to be sent
    :param queue_config: dict config of consumer queues: {'exchange': '', 'queues': [], 'routing_key': '',
    'exchange_type' (optional): '', 'error_messaging': dict}
    :return: None
    """
    loop = None
    if 'exchange_type' not in queue_config:
        queue_config['exchange_type'] = 'direct'
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(loop.create_task(
            send_message_to_exchange(rabbitmq_config, queue_config, message)))
    finally:
        if loop is not None:
            loop.close()


def send_bulk_messages(rabbitmq_config: dict, queue_config: dict, messages: list) -> None:
    """
    Send bulk messages to rabbitmq queues.
    :param rabbitmq_config: dict config for rabbitmq instance config: {'host': , 'port': , 'username': , 'password': }
    :param messages: list of dict object(message) to be sent
    :param queue_config: dict config of consumer queues: {'exchange': '', 'queues': [], 'routing_key': '',
    'exchange_type':'', 'error_messaging': dict}
    :return:
    """
    loop = None
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(loop.create_task(
            send_bulk_messages_to_exchange(rabbitmq_config, queue_config, messages)))
    finally:
        if loop is not None:
            loop.close()


async def send_request_to_error_queue(rabbitmq_config: dict, error_messaging_queue: dict, error_message: dict) -> None:
    """
    Send message to error while publishing message to queue
    :param rabbitmq_config Rabbitmq instance config
    :param error_messaging_queue Error queue config
    :param error_message Error message to be sent to queue
    """
    send_message(rabbitmq_config, error_messaging_queue, error_message)
