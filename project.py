import RPi.GPIO as GPIO
import time
from smbus import SMBus

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#Sei GPIO pin
trigger = 23
echo = 24
addr = 0x9 #bus address
bus = SMBus(1) #indicate device

GPIO.setup(trigger,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)

def distance():
    #set trigger to HIGH
    GPIO.output(trigger,True)
    time.sleep(0.00001)
    #after 0.00001s, set to LOW
    GPIO.output(trigger,False)
    
    start = time.time()
    stop = time.time()
    
    #save start time
    while GPIO.input(echo)==0:
        start = time.time()
    #save stop time
    while GPIO.input(echo)==1:
        stop = time.time()
    
    #time difference start and arrival
    gap = stop-start
    
    #sonic speed is 343000 cm/s, and there are go and back
    #so divided by 2
    dis = (gap*34300)/2
    
    return dis

#looping untill KeyboardInterrupt
i = 1
try:
    while i == 1:
        dis = distance()
        
        if dis<100:
            bus.write_byte(addr, 0x0)
        elif dis>100:
            bus.write_byte(addr, 0x1)
        else:
            i=0
        time.sleep(0.1)

#break the loop when KeyboardInterrupt (control+c)
except KeyboardInterrupt:
    GPIO.cleanup()#cleanup pins