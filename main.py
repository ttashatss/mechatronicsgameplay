# Copyright 2021 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Main script to run the object detection routine."""
import argparse
import sys
import time
import socketio

import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils as ut

sio = socketio.Client()

#Stepping Motor Nema 17 (US-17HS4401S)
from time import sleep
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

#Button setting up
GPIO.setmode(GPIO.BCM)         #Set GPIO pin numbering
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Enable input and pull up resistors

#Laser setting
GPIO.setup(17,GPIO.OUT)


#-----------------------------------------------------------------------------
#Motor Setting
#Define GPIO Pins
GPIO_pins = (14, 15, 18) #Microstep Resolution MS1-MS3
direction =20
step = 21

#Declare an named instance of class pass GPIO pins numbers
mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")

#first parameter: True = CW = Turn Right
def cw():
    return mymotortest.motor_go(True, "Full", 200, .01, False, .05)

#first parameter: False = CCW = Turn Left
def ccw():
    return mymotortest.motor_go(False, "Full", 200, .01, False, .05)

#stop motor
def stop():
    return mymotortest.motor_stop()


global pigCaseX
pigCaseX = -1

global buttonPressed
buttonPressed = False 

#-----------------------------------------------------------------------------
#camera setting
@sio.on('run')
def run(model: str, camera_id: int, width: int, height: int, num_threads: int,
        enable_edgetpu: bool, username:str) -> None:
  """Continuously run inference on images acquired from the camera.

  Args:
    model: Name of the TFLite object detection model.
    camera_id: The camera id to be passed to OpenCV.
    width: The width of the frame captured from the camera.
    height: The height of the frame captured from the camera.
    num_threads: The number of CPU threads to run the model.
    enable_edgetpu: True/False whether the model is a EdgeTPU model.
  """

  # Variables to calculate FPS
  counter, fps = 0, 0
  start_time = time.time()

  # Start capturing video input from the camera
  cap = cv2.VideoCapture(camera_id)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

  # Visualization parameters
  row_size = 20  # pixels
  left_margin = 24  # pixels
  text_color = (0, 0, 255)  # red
  font_size = 1
  font_thickness = 1
  fps_avg_frame_count = 10

  # Initialize the object detection model
  base_options = core.BaseOptions(
      file_name=model, use_coral=enable_edgetpu, num_threads=num_threads)
  detection_options = processor.DetectionOptions(
      max_results=3, score_threshold=0.3)
  options = vision.ObjectDetectorOptions(
      base_options=base_options, detection_options=detection_options)
  detector = vision.ObjectDetector.create_from_options(options)
  
  #initialize pigCase
#   global pigCaseX
#   pigCaseX = -1

  #dimension of the frame
  frameW = 640
  frameH = 480
  
  minW = 3*frameW/8
  maxW = 5*frameW/8
  
  #Button
#   global buttonPressed
#   buttonPressed = False     

  # Continuously capture images from the camera and run inference
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      sys.exit(
          'ERROR: Unable to read from webcam. Please verify your webcam settings.'
      )

    counter += 1
    image = cv2.flip(image, 1)

    # Convert the image from BGR to RGB as required by the TFLite model.
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create a TensorImage object from the RGB image.
    input_tensor = vision.TensorImage.create_from_array(rgb_image)

    # Run object detection estimation using the model.
    detection_result = detector.detect(input_tensor)
    
    #processing coordinate of picture to classify the case
    if detection_result.detections != []:
        #If detect as green-pig
        if detection_result.detections[0].categories[0].category_name == 'green-pig':
            # print(detection_result.detections[0].bounding_box)
            #origin at top-left
            originX = detection_result.detections[0].bounding_box.origin_x
            originY = detection_result.detections[0].bounding_box.origin_y
            #image size
            width = detection_result.detections[0].bounding_box.width
            height = detection_result.detections[0].bounding_box.height
            #locate center of picture
            centerX = originX + width/2
            centerY = originY + height/2
            # print(centerX,centerY)
            
            if centerX < minW:
                pigCaseX = 0     #too left
            elif centerX > minW and centerX < maxW:
                pigCaseX = 1     #middle
            elif centerX > maxW:
                pigCaseX = 2     #too right
    else:
        pigCaseX = -1
 
    #print pigCaseX
    # print(pigCaseX)
    
    if pigCaseX == 0:                      #too left
        cw()
    elif pigCaseX == 1:                    #middle 
        stop()
    elif pigCaseX == 2:                     #too right
        ccw()
    
    #if pig is not detected, the motor will keep rotating
    
    #setting button
    buttonPressed = not GPIO.input(24) #Read and store value of input to a variable
    if buttonPressed == True:       #Check whether pin is grounded
    #  #Print 'Button Pressed'
       #open laser when button is pressed
      print([username, pigCaseX, buttonPressed])
      # sio.emit('mechanics', [username, pigCaseX, buttonPressed])
      GPIO.output(17,1) 
      time.sleep(0.5)              #Delay of 0.1s
      GPIO.output(17,0) 
      time.sleep(0.5)              #Delay of 0.9s    
          
    # Draw keypoints and edges on input image
    image = ut.visualize(image, detection_result)

    # Calculate the FPS
    if counter % fps_avg_frame_count == 0:
      end_time = time.time()
      fps = fps_avg_frame_count / (end_time - start_time)
      start_time = time.time()

    # Show the FPS
    fps_text = 'FPS = {:.1f}'.format(fps)
    text_location = (left_margin, row_size)
    cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                font_size, text_color, font_thickness)

    # Stop the program if the ESC key is pressed.
    if cv2.waitKey(1) == 27:
      break
    cv2.imshow('object_detector', image)

    print([pigCaseX, buttonPressed])
    sio.emit('mechanics', [username, pigCaseX, buttonPressed])

  cap.release()
  cv2.destroyAllWindows()


# def main(username):
#   parser = argparse.ArgumentParser(
#       formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#   parser.add_argument(
#       '--model',
#       help='Path of the object detection model.',
#       required=False,
#       default='pigModel.tflite')
#   parser.add_argument(
#       '--cameraId', help='Id of camera.', required=False, type=int, default=0)
#   parser.add_argument(
#       '--frameWidth',
#       help='Width of frame to capture from camera.',
#       required=False,
#       type=int,
#       default=640)
#   parser.add_argument(
#       '--frameHeight',
#       help='Height of frame to capture from camera.',
#       required=False,
#       type=int,
#       default=480)
#   parser.add_argument(
#       '--numThreads',
#       help='Number of CPU threads to run the model.',
#       required=False,
#       type=int,
#       default=4)
#   parser.add_argument(
#       '--enableEdgeTPU',
#       help='Whether to run the model on EdgeTPU.',
#       action='store_true',
#       required=False,
#       default=False)
#   args = parser.parse_args()

#   run(args.model, int(args.cameraId), args.frameWidth, args.frameHeight,
#       int(args.numThreads), bool(args.enableEdgeTPU), username)


# if __name__ == '__main__':
#   main()

@sio.event
def connect():
    print("mechanics connected!")
    sio.emit('client3', 'connected')

@sio.on('toclient3')
def toclient2(data) :
    print('client3', data)
    parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
      '--model',
      help='Path of the object detection model.',
      required=False,
      default='pigModel.tflite')
    parser.add_argument(
      '--cameraId', help='Id of camera.', required=False, type=int, default=0)
    parser.add_argument(
      '--frameWidth',
      help='Width of frame to capture from camera.',
      required=False,
      type=int,
      default=640)
    parser.add_argument(
      '--frameHeight',
      help='Height of frame to capture from camera.',
      required=False,
      type=int,
      default=480)
    parser.add_argument(
      '--numThreads',
      help='Number of CPU threads to run the model.',
      required=False,
      type=int,
      default=4)
    parser.add_argument(
      '--enableEdgeTPU',
      help='Whether to run the model on EdgeTPU.',
      action='store_true',
      required=False,
      default=False)
    args = parser.parse_args()

    run(args.model, int(args.cameraId), args.frameWidth, args.frameHeight,
      int(args.numThreads), bool(args.enableEdgeTPU), data)


sio.connect("http://localhost:8000")