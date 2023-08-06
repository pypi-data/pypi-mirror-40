from rabbitmq_asynqp.rabbitmq_consumer import consume_message


class Consumer:

    def __init__(self, rabbitmq_config: dict, queue: str, callback_fn):
        self.rabbitmq_config = rabbitmq_config
        self.queue = queue
        self.callback_fn = callback_fn

    def __call__(self, *args, **kwargs):
        consume_message(rabbitmq_config=self.rabbitmq_config, queue=self.queue, callback_fn=self.callback_fn)