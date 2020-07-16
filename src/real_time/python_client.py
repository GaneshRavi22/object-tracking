from confluent_kafka import Consumer
import pickle
import logging
import cv2

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)

BROKER_URL = 'localhost:9092'
TOPIC_NAME = 'topic2'


def read_frames():
    c = Consumer({
        'bootstrap.servers': BROKER_URL,
        'group.id': 'mygroup',
        'auto.offset.reset': 'earliest',
        'fetch.message.max.bytes': 50000000
    })

    c.subscribe([TOPIC_NAME])

    while True:
        msg = c.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue

        frame = pickle.loads(msg.value())
        cv2.imshow('Consumer', frame)
        if cv2.waitKey(1) == 27:
            break  # esc to quit

    cv2.destroyAllWindows()
    c.close()


if __name__ == "__main__":
    read_frames()
