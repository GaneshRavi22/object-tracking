# Real-time Object Detection Using Tensorflow

## Assumptions:
<PROJECT_ROOT> represents the full path where this GIT repo is cloned.

## Pre-requisites:
1. GIT Installed
2. Python3 and pip configured
3. Build tools for OpenCV
	On Windows:
	------------
	Install Microsoft C++ Build tools by following the steps below:
	* Go to => https://visualstudio.microsoft.com/visual-cpp-build-tools/
	* Click on "Download Build tools"
	* Open the installer and install "Visual Studio Build Tools 2019"
		
	On Linux:
	---------
	```bash
	sudo apt update
	sudo apt install python3-opencv
	```

## Installing required Python Libraries
* Install the below required standard standard libraries
	```bash
	pip install opencv-python
	pip install tensorflow
	pip install jupyter
	pip install cython
	pip install matplotlib
	pip install contextlib2
	pip install pillow
	pip install lxml
	```

* Install the COCO API library  
	On Windows:
    ```bash
    pip install git+https://github.com/philferriere/cocoapi.git#subdirectory=PythonAPI 
    ```

	On Linux:
	```bash
	pip install pycocotools
    ```

## Download and setup the latest Object detection Tensorflow models
* Clone the required folder from Tensorflow Git repo:
	```bash
	cd <PROJECT_ROOT>
	git clone --depth 1 https://github.com/tensorflow/models
	cd models/research/
	```
* Setup Google Protobuf since Tensorflow requires it:
	```bash
	cd <PROJECT_ROOT>
	wget https://github.com/protocolbuffers/protobuf/releases/download/v3.12.3/protoc-3.12.3-win64.zip
	unzip protoc-3.12.3-win64.zip
	rm protoc-3.12.3-win64.zip
	cd models/research/
	bin/protoc object_detection/protos/*.proto --python_out=.
	```
	
	On Windows, open Powershell and run the following commands:
	```bash
	cd <PROJECT_ROOT>
	wget https://github.com/protocolbuffers/protobuf/releases/download/v3.12.3/protoc-3.12.3-win64.zip -outfile protoc.zip
	Expand-Archive -LiteralPath protoc.zip -DestinationPath .
	rm protoc.zip
	cd models/research/
	bin/protoc.exe object_detection/protos/*.proto --python_out=.
	```
* Install the Object Detection code as a library with the following commans:
	```bash
	cd <PROJECT_ROOT>/models/research
	pip install .
	```
	
## Running the Ream-time Object Detection from Default Video device

### From Notebook
Execute the downloaded `<PROJECT_ROOT>/noteooks/object-detection-real-time.ipynb` Notebook. The last cell will start a new Window which renders the video from the default video office on the machine, with the output bounding boxes from the Object Detection model.

### Python File
Run the following command to start the application:
```bash
python src/detection/real_time.py "<PROJECT_ROOT>/models"
```

## Real-time Execution using Kafka
1. Run the following commands to bring up the Kafka containers:
    ```bash
    cd <project_root>
    docker-compose up -d
    ```
2. Install the following pip package
    ```bash
    pip install confluent-kafka
   ```
3. Execute the following command to run the Producer process which will capture frames and send to Kafka topic
    ```bash
   python src/messaging/frame_producer.py 
   ```
   This process also open a Window titled `Producer` where the frames read from webcam will be displayed.
4. Execute the following command to run the Consumer process which will read frames from the Kafka topic
    ```bash
   python src/messaging/frame_consumer.py 
   ```
   This process also open a Window titled `Consumer` where the frames read from the Kafka topic will be displayed.
   