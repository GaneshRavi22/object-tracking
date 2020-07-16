from flask import Flask, render_template, Response
from confluent_kafka import Consumer
import pickle
import cv2
import logging

from real_time.kafka_utils import Kafka


BROKER_URL = 'localhost:9092'
TOPIC_NAME = 'topic2'


app = Flask(__name__)
log = logging.getLogger(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def gen():
    kafka = Kafka(BROKER_URL)
    kafka.delete_topic(TOPIC_NAME)
    kafka.create_topic(TOPIC_NAME)

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
        (flag, jpeg_frame) = cv2.imencode(".jpg", frame)

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               jpeg_frame.tobytes() + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000', debug=True)