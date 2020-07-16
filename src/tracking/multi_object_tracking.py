from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import time
import cv2
from random import randint

# "csrt": cv2.TrackerCSRT_create,
# "kcf": cv2.TrackerKCF_create,
# "boosting": cv2.TrackerBoosting_create,
# "mil": cv2.TrackerMIL_create,
# "tld": cv2.TrackerTLD_create,
# "medianflow": cv2.TrackerMedianFlow_create,
# "mosse": cv2.TrackerMOSSE_create

multi_tracker = cv2.MultiTracker_create()

init_bboxes = []
colors = []

vs = VideoStream(src=0).start()
time.sleep(1.0)

fps = None

while True:
    frame = vs.read()

    frame = imutils.resize(frame, width=500)
    (H, W) = frame.shape[:2]

    if len(init_bboxes) > 0:
        (success, boxes) = multi_tracker.update(frame)
        # if success:
        #     (x, y, w, h) = [int(v) for v in boxes]
        #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        for i, box in enumerate(boxes):
            p1 = (int(box[0]), int(box[1]))
            p2 = (int(box[0] + box[2]), int(box[1] + box[3]))
            cv2.rectangle(frame, p1, p2, colors[i], 2, 1)

        fps.update()
        fps.stop()

        info = [
            ("Success", "Yes" if success else "No"),
            ("FPS", "{:.2f}".format(fps.fps())),
        ]

        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        while True:
            bbox = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
            print(bbox)
            print(type(bbox))
            init_bboxes.append(bbox)
            colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
            multi_tracker.add(cv2.TrackerCSRT_create(), frame, bbox)

            key = cv2.waitKey(0) & 0xFF
            if key == ord("d"):
                break

        fps = FPS().start()

    elif key == ord("q"):
        break

vs.stop()
cv2.destroyAllWindows()