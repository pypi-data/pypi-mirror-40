===============
rabbitmq_asynqp
===============

Usage:
======

* Both producer and consumer:
-----------------------------

rabbitmq_asynqp provides you ability to use rabbitmq messaging asynchronous non-blocking way by the use of asynqp and
asyncio with just few lines of code. Typical usage will be like this:


        from rabbitmq_asynqp.messaging import Messaging

        rabbitmq_config = dict(host="localhost", port=5672, username="guest", password="guest")
        queue_config = dict(
                exchange="sample_exchange",
                queues=["sample_queue1"],
                routing_key="sample.routing_key",
                exchange_type="direct",
                error_messaging=dict(
                    exchange="error_exchange",
                    queues=["error_queue"],
                    routing_key="error.key",
                    exchange_type="direct",
                )
            )

        queue_settings = {'reconnect_backoff_secs': 1, 'connection_check_polling_secs': 5} # Not compulsory

        def consumer_func(message: dict):
            # define your consumer func
            pass

        messaging = Messaging(rabbitmq_config: dict, queue_config: dict, consumer_func)

use this messaging object globally for sending message like this:

        messaging.send_message(message) # To send single message
        messaging.send_messages(messages) # To send multiple bulk messages

* Only Consumer:
----------------

To run only consumer use a separate thread or process and do following:

        from rabbitmq_asynqp.messaging import Consumer

        rabbitmq_config = dict(host="localhost", port=5672, username="guest", password="guest")
        queue = "queue_name"
        queue_settings = {'reconnect_backoff_secs': 1, 'connection_check_polling_secs': 5} # Not compulsory

        def consumer_func(message:dict):
            # define your consumer func
            pass

        consumer = Consumer(rabbitmq_config, queue, consumer_func, queue_settings)
        consumer()


* Only Producer:
----------------

To run producer only for message production:

        from rabbitmq_asynqp.messaging import Producer

        rabbitmq_config = dict(host="localhost", port=5672, username="guest", password="guest")
        queue_config = dict(
                exchange="sample_exchange",
                queues=["sample_queue1"],
                routing_key="sample.routing_key",
                exchange_type="direct",
                error_messaging=dict(
                    exchange="error_exchange",
                    queues=["error_queue"],
                    routing_key="error.key",
                    exchange_type="direct",
                )
            )

        producer = Producer(rabbitmq_config, queue_config)
        producer.send_msg(message)


Message sent must be dict.

For any queries, mail to akshay2agarwal@gmail.com