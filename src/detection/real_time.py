import sys
import os
import numpy as np
import tensorflow as tf
import pathlib
import cv2

from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util


def load_model(model_name):
    base_url = 'http://download.tensorflow.org/models/object_detection/'
    model_file = model_name + '.tar.gz'
    model_dir = tf.keras.utils.get_file(
    fname=model_name,
    origin=base_url + model_file,
    untar=True)

    model_dir = pathlib.Path(model_dir)/"saved_model"

    model = tf.saved_model.load(str(model_dir))
    model = model.signatures['serving_default']
    return model


def run_inference_for_single_image(model, image):
    image = np.asarray(image)
    input_tensor = tf.convert_to_tensor(image)
    input_tensor = input_tensor[tf.newaxis,...]

    output_dict = model(input_tensor)

    num_detections = int(output_dict.pop('num_detections'))
    output_dict = {key:value[0, :num_detections].numpy()
                 for key,value in output_dict.items()}
    output_dict['num_detections'] = num_detections

    # detection_classes should be ints.
    output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)

    # Handle models with masks:
    if 'detection_masks' in output_dict:
        # Reframe the the bbox mask to the image size.
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                  output_dict['detection_masks'], output_dict['detection_boxes'],
                   image.shape[0], image.shape[1])
        detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5,
                                           tf.uint8)
        output_dict['detection_masks_reframed'] = detection_masks_reframed.numpy()

    return output_dict


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("The full path to the cloned 'models' folder should be given as an argument")
        print("Usage:")
        print("python object_detector.py /home/username/models")
        raise ValueError("Required argument not passed!")

    # List of the strings that is used to add correct label for each box.
    PATH_TO_LABELS = os.path.join(str(sys.argv[1]), "research", "object_detection", "data", "mscoco_label_map.pbtxt")
    category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

    model_name = 'ssd_mobilenet_v1_coco_2018_01_28'
    detection_model = load_model(model_name)

    cam = cv2.cv2.VideoCapture(0)

    while (True):
        ret, frame = cam.read()

        image_np = np.array(frame)
        # Run the Objection model
        output_dict = run_inference_for_single_image(detection_model, image_np)
        print(output_dict)

        # Visualization of the results of detection on the original frame
        vis_util.visualize_boxes_and_labels_on_image_array(
          image_np,
          output_dict['detection_boxes'],
          output_dict['detection_classes'],
          output_dict['detection_scores'],
          category_index,
          instance_masks=output_dict.get('detection_masks'),
          use_normalized_coordinates=True,
          line_thickness=8)
        cv2.imshow('image', cv2.resize(image_np,(1000,800)))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    cam.release()
