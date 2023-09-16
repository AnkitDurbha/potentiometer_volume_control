
from pynput.keyboard import Key,Controller
import time
from ADCDevice import *

adc = ADCDevice() # Define an ADCDevice class object

def setup():
    global adc
    if(adc.detectI2C(0x48)): # Detect the pcf8591.
        adc = PCF8591()
    elif(adc.detectI2C(0x4b)): # Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
        "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
        "Program Exit. \n")
        exit(-1)
        
def loop():
    lastValue = 0
    keyboard = Controller()
    value = 1
    while True:
        value = adc.analogRead(0)    # read the ADC value of channel 0
        if value > 200:
            value = 200
        
        value /= 20
        round(value, 0)
        value = int(value)
        if value > lastValue:    
            for i in range(value - lastValue):
                keyboard.press(Key.media_volume_down)
        else:
            for i in range(lastValue - value):
                keyboard.press(Key.media_volume_up)
        lastValue = value
        

def destroy():
    adc.close()
    
if __name__ == '__main__':   # Program entrance
    print ('Program is starting ... ')
    try:
        setup()
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()