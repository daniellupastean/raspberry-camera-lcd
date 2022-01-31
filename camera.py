import RPi.GPIO as GPIO
import time
from time import sleep



import base64
from picamera import PiCamera

import requests as req
from requests.structures import CaseInsensitiveDict

camera = PiCamera()
camera.resolution=(2592,1944)
camera.framerate = 15

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 18
GPIO_ECHO = 24

GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)

def distance():
    GPIO.output(GPIO_TRIGGER, True)
    
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    
    StartTime = time.time()
    StopTime = time.time()
    
    while GPIO.input(GPIO_ECHO)==0:
        StartTime = time.time()
        
    while GPIO.input(GPIO_ECHO)==1:
        StopTime = time.time()
        
    TimeElapsed = StopTime - StartTime
    
    distance = (TimeElapsed * 34300) / 2
    return distance;

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            #print("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
            if dist <= 50:
                camera.start_preview()
                camera.capture('/home/pi/Desktop/ProiectMC/images/image.jpg') 
                sleep(6)
                camera.stop_preview()
                with open("/home/pi/Desktop/ProiectMC/images/image.jpg","rb") as img_file:
                    b64_string = base64.b64encode(img_file.read())
                    headers = CaseInsensitiveDict()
                    headers["Accept"] = "application/json"
                    headers["Authorization"] = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImU0ZTdlZTI5LTBiZTYtNDBkMi04NjBlLTc0YzY4ZTAzYjlmNSIsInJvbGUiOiJ1c2VyIiwiaWF0IjoxNjQwOTE2Mjk1LCJleHAiOjE2NDEwMDI2OTV9.MDhCx_TUYQU4muDYcx6y7BVqSj5csJffOWClZifBFwc"
                    r = req.post('http://imageverse-api.herokuapp.com/gallery', data={"picture":b64_string.decode('utf-8')}, headers=headers)
                    #print(b64_string.decode('utf-8'))
                    print(r.text)
                
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()