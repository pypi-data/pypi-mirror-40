#!/usr/bin/env python

from rabbitmq_asynqp.messaging import Messaging

if __name__ == "__main__":
    rabbitmq_config = dict(host="localhost", port=5672, username="guest", password="guest")
    queue_config = dict(
        exchange="rabbit_sample_exchange",
        queues=["sample_queue"],
        routing_key="sample.routing_key",
        exchange_type="direct"
    )

    def print_callback(msg):
        print(msg)

    # Use this as a global object
    messaging = Messaging(rabbitmq_config=rabbitmq_config, queue_config=queue_config, consumer_func=print_callback)

    messaging.send_message({"msg_i": 1})
