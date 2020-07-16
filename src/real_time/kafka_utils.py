import logging

from confluent_kafka.admin import AdminClient, NewTopic

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)

class Kafka:

    def __init__(self, broker_url):
        self.broker_url = broker_url
        self.admin_client = self._get_admin_client()

    def _get_admin_client(self):
        return AdminClient({'bootstrap.servers': self.broker_url})

    def create_topic(self, topic_name):
        new_topics = [NewTopic(topic_name, num_partitions=1, replication_factor=1)]

        fs = self.admin_client.create_topics(new_topics, request_timeout=2)

        # Wait for each operation to finish.
        for topic, f in fs.items():
            try:
                f.result()
                log.info("Topic {} created".format(topic))
            except Exception as e:
                log.error("Failed to create topic {}: {}".format(topic, e))

    def delete_topic(self, topic_name):
        fs = self.admin_client.delete_topics([topic_name], request_timeout=2)

        # Wait for each operation to finish.
        for topic, f in fs.items():
            try:
                f.result()
                log.info("Topic {} deleted".format(topic))
            except Exception as e:
                log.error("Failed to delete topic {}: {}".format(topic, e))


if __name__ == "__main__":
    kafka = Kafka('localhost:9092')
    kafka.create_topic('test')