from rabbitmq_asynqp.rabbitmq_producer import send_message, send_bulk_messages


class Producer:

    def __init__(self, rabbitmq_config: dict, queue_config: dict):
        self.rabbitmq_config = rabbitmq_config
        self.queue_config = queue_config

    def send_msg(self, message: dict):
        send_message(rabbitmq_config=self.rabbitmq_config, queue_config=self.queue_config, message=message)

    def send_msgs(self, messages: list):
        send_bulk_messages(rabbitmq_config=self.rabbitmq_config, queue_config=self.queue_config, messages=messages)
