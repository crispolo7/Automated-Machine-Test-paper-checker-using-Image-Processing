import RPi.GPIO as GPIO
from picamera import PiCamera
import time

def scan():
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(4, GPIO.OUT)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)

    GPIO.setup(6, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(19, GPIO.OUT)
    GPIO.setup(26, GPIO.OUT)

    GPIO.setup(12,GPIO.IN,pull_up_down=GPIO.PUD_UP) #Paper detector switch
    GPIO.setup(2,GPIO.IN) #Start button
    GPIO.setup(14,GPIO.OUT) #Servo motor

    camera = PiCamera()  #Camera
    count = 0

    GPIO.output(4, True)
    GPIO.output(17, True)
    GPIO.output(6, True)
    GPIO.output(13, True)

    while True:
        if (GPIO.input(2)== False):
            print("Start scanning")

            GPIO.output(21, True)   #DC motor
            GPIO.output(22, False)
            time.sleep(1)

            GPIO.setmode(GPIO.BCM)  #Servo motor
            pwm=GPIO.PWM(14,50)
            pwm.start(7.5)
            pwm.ChangeDutyCycle(11.5)
            time.sleep(0.4)
            pwm.ChangeDutyCycle(7.5)
            time.sleep(0.4)
            pwm.stop()

            GPIO.output(21, False)
            GPIO.output(22, False)
            time.sleep(.5)

            if (GPIO.input(12)== False):
                print("Paper swallowed")

                GPIO.output(21, True)
                GPIO.output(22, False)
                time.sleep(1.32)

                GPIO.setmode(GPIO.BCM)
                pwm=GPIO.PWM(14,50)
                pwm.start(7.5)
                pwm.ChangeDutyCycle(7.5)
                time.sleep(1)
                pwm.stop()

                GPIO.output(21, False)
                GPIO.output(22, False)
                time.sleep(0.8)

                camera.rotation = 0
                camera.framerate = 80
                count+=1
                #camera.start_preview()
                for i in range(count):
                    time.sleep(.025)
                camera.capture('/home/pi/Desktop/Foler/image%03d.jpg'% count)
                #camera.stop_preview()

                GPIO.output(21, True)
                GPIO.output(22, False)
                time.sleep(.2)

                GPIO.output(21, False)
                GPIO.output(22, False)
                time.sleep(1)

                GPIO.output(19, True)
                GPIO.output(26, False)
                time.sleep(2)

                GPIO.output(19, False)
                GPIO.output(26, False)
                time.sleep(.5)

            else:
                GPIO.cleanup()



        time.sleep(0.2)
    return count