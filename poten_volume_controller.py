from pynput.keyboard import Key,Controller
from ADCDevice import *

adc = ADCDevice() # Define an ADCDevice class object

def setup():
    global adc
    if(adc.detectI2C(0x4b)): # Detect the ADC
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
        "Program Exit. \n")
        exit(-1)
        
def main():
    lastValue = 0
    keyboard = Controller()
    value = 1
    while True:
        value = adc.analogRead(0)    # read the ADC value
        if value > 200:   # Rounding off the value
            value = 200
        value /= 20
        round(value, 0)
        value = int(value)
        if value > lastValue:    # Simulating key presses, depending on which direction the potentiometer has been moved
            for i in range(value - lastValue):
                keyboard.press(Key.media_volume_down)
        if lastValue > value:
            for i in range(lastValue - value):
                keyboard.press(Key.media_volume_up)
        lastValue = value     # Setting lastValue = to value so we know what direction the potentiometer was turned on the last iteration of the loop
        

def destroy():
    adc.close()
    
if __name__ == '__main__':   # Program entrance
    print ('Program is starting ... ')
    try:
        setup()
        main()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()