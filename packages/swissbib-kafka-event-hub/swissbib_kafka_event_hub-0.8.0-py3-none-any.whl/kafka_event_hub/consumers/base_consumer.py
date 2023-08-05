from kafka_event_hub.config import BaseConfig

from confluent_kafka.admin import AdminClient, ClusterMetadata
from confluent_kafka import Consumer, Message, TopicPartition

from typing import List
import logging


class AbstractBaseConsumer(object):

    def __init__(self, config: str, config_class: type(BaseConfig), logger=logging.getLogger(__name__)):
        """

        Consumer configs:
        
        """
        self._configuration = config_class(config)
        self._admin = AdminClient(**self._configuration['AdminClient'])
        self._consumer = Consumer(**self._configuration['Consumer'])
        self._logger = logger
        self.subscribe(self._configuration['Topic'])

    @property
    def configuration(self):
        return self._configuration

    @property
    def assignment(self) -> List[TopicPartition]:
        return self._consumer.assignment()

    def close(self):
        self._consumer.close()

    def subscribe(self, topics: List[str]):
        self._consumer.subscribe(topics)

    def unsubscribe(self):
        self._consumer.unsubscribe()

    def consume(self, num_messages: int = 1, timeout: int = -1) -> List[Message]:
        return self._consumer.consume(num_messages=num_messages, timeout=timeout)

    def list_topics(self, topic: str = None, timeout: int = -1) -> ClusterMetadata:
        return self._consumer.list_topics(topic, timeout)

    def delete_topic(self):
        fs = self._admin.delete_topics(self._configuration['Topic'], operation_timeout=30)

        for topic,f in fs.items():
            try:
                f.result()
                self._logger.info('Topic %s created.', topic)
            except Exception as e:
                self._logger.error('Failed to create topic %s: %s', topic, e)




