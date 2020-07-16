from confluent_kafka import Producer
import cv2
import pickle
from time import sleep
import logging

from messaging.kafka_utils import Kafka


logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)


BROKER_URL = 'localhost:9092'
TOPIC_NAME = 'topic1'
FRAMES_PER_SECOND = 10


def send_message(message):
    producer = Producer({
        'bootstrap.servers': BROKER_URL,
        'message.max.bytes': 50000000
    })

    producer.produce(TOPIC_NAME, message)
    producer.flush()


def send_frames():
    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()
        cv2.imshow("Producer", frame)
        serialized_image_np = pickle.dumps(frame, protocol=0)
        send_message(serialized_image_np)
        if cv2.waitKey(1) == 27:
            break  # esc to quit

        sleep(1 / FRAMES_PER_SECOND)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    kafka = Kafka(BROKER_URL)
    kafka.delete_topic(TOPIC_NAME)
    kafka.create_topic(TOPIC_NAME)
    send_frames()