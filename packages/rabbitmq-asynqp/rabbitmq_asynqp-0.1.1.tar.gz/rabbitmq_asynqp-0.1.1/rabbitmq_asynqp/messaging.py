from rabbitmq_asynqp.consumer import Consumer
from rabbitmq_asynqp.producer import Producer
from concurrent.futures import ThreadPoolExecutor


class Messaging:
    def __init__(self, rabbitmq_config: dict, queue_config: dict, consumer_func, queue_settings: dict = None):
        self.rabbitmq_config = rabbitmq_config
        self.queue_config = queue_config
        self.consumer_func = consumer_func
        self.queue_settings = queue_settings
        self.queue_consumer_locks = False
        queue_consumer_pool = ThreadPoolExecutor(max_workers=len(self.queue_config["queues"]))
        for queue in self.queue_config["queues"]:
            queue_consumer_pool.submit(self.__run_consumer, **{'queue': queue})
        self.queue_consumer_locks = True

    def __run_consumer(self, queue: str):
        consumer = Consumer(self.rabbitmq_config, queue, self.consumer_func, self.queue_settings)
        consumer()

    def send_message(self, message: dict):
        if not self.queue_consumer_locks:
            queue_consumer_pool = ThreadPoolExecutor(max_workers=len(self.queue_config["queues"]))
            for queue in self.queue_config["queues"]:
                queue_consumer_pool.submit(self.__run_consumer, **{'queue': queue})
            self.queue_consumer_locks = True
        producer = Producer(self.rabbitmq_config, self.queue_config)
        producer.send_msg(message)

    def send_messages(self, messages: list):
        if not self.queue_consumer_locks:
            queue_consumer_pool = ThreadPoolExecutor(max_workers=len(self.queue_config["queues"]))
            for queue in self.queue_config["queues"]:
                queue_consumer_pool.submit(self.__run_consumer, **{'queue': queue})
            self.queue_consumer_locks = True
        producer = Producer(self.rabbitmq_config, self.queue_config)
        producer.send_msgs(messages)
