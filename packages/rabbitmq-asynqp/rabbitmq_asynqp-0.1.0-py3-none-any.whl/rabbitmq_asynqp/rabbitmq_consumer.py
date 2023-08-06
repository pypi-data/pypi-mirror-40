import asyncio
import asynqp


class EventConsumer:

    def __init__(self, callback_fn, queue):
        self.callback_fn = callback_fn
        self.queue = queue

    def __call__(self, msg):
        """
        Whenever call is called same message content is processed and ack is sent to rabbit mq
        :param msg: Rabbitmq message object
        :return: None
        """
        self.callback_fn(msg.json())
        msg.ack()

    def on_error(self, exc):
        print("While consuming QUEUE:{queue} following error occurred: {exc}".
              format(queue=self.queue, exc=exc))

    def on_cancel(self):
        print("Stopping consumer for QUEUE:{queue}".format(queue=self.queue))


async def connect_and_consume(rabbitmq_config, callback_fn, queue):
    """
    Creates a new connection and starts Consumer. Do not use this directly.
    :param rabbitmq_config: Rabbit mq config dict for connection
    {'host': , 'port': , 'username': , 'password'}
    :param queue: rabbit mq QUEUE name to be consumed (str)
    :return: Rabbitmq connection object
    """
    try:
        connection = await asynqp.connect(rabbitmq_config['host'], rabbitmq_config['port'],
                                          rabbitmq_config['username'], rabbitmq_config['password'])
    except Exception as e:
        print(e)
        return None
    try:
        channel = await connection.open_channel()
        amqp_queue = await channel.declare_queue(queue)
        await amqp_queue.consume(EventConsumer(callback_fn, queue))
    except asynqp.AMQPError as err:
        print("Could not consume QUEUE:{queue}".format(queue=queue))
        print(err)
        await connection.close()
        return None
    return connection


async def reconnector(rabbitmq_config, callback_fn, queue):
    """
    Reconnection to rabbit mq by internal polling. Don't use this directly.
    :param rabbitmq_config: Rabbit mq config dict for connection
    {'host': , 'port': , 'username': , 'password'}
    :param event_queue: Asyncio QUEUE contain messages
    :param queue: rabbit mq QUEUE name (str)
    :return: None
    """
    connection = None
    queue_settings = {'reconnect_backoff_secs': 1, 'connection_check_polling_secs': 5}
    connection_failures = 0
    try:
        while True:
            if connection is None or connection.is_closed():
                try:
                    connection = await connect_and_consume(rabbitmq_config, callback_fn, queue)
                except (ConnectionError, OSError) as e:
                    connection = None
                    connection_failures += 1
                    print("Unable to establish connection and consume QUEUE:{queue}, failure count"
                                               ":{failures}".format(queue=queue, failures=connection_failures))
                    print(e)
                if connection is None:
                    await asyncio.sleep(queue_settings['reconnect_backoff_secs']*connection_failures)

            # poll connection state check
            await asyncio.sleep(queue_settings["connection_check_polling_secs"])
    except asyncio.CancelledError as err:
        if connection is not None:
            await connection.close()
            print("Connection closed for consumer in QUEUE: {queue}".format(queue=queue))


def consume_message(rabbitmq_config, queue, callback_fn):
    """
    Consumer creation for QUEUE.
    :param app: flask app object
    :param rabbitmq_config: Rabbit mq config dict for connection
    {'host': , 'port': , 'username': , 'password'}
    :param queue: rabbit mq QUEUE name (str)
    :param callback_fn: consumer function to be used
    :return: None
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # Start main connecting and consuming task in the background
    reconnect_task = loop.create_task(reconnector(rabbitmq_config, callback_fn, queue))
    try:
        loop.run_until_complete(reconnect_task)
    except asyncio.CancelledError:
        reconnect_task.cancel()
        loop.run_until_complete(reconnect_task)
        print("Asyncio coroutine cancelled")
    finally:
        for task in asyncio.tasks.all_tasks(loop):
            task.cancel()
        loop.close()
        print("Consumer for QUEUE:{queue} stopped.".format(queue=queue))
