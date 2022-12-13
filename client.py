import machine
from machine import Timer, Pin, RTC, ADC
import time
from IMU import *
import ssd1306
import network
import usocket as socket
import time
import json
import sh1106
from button import Button
from hcsr04 import HCSR04
import urequests as requests

def update_display(timer):
    global current_exericise_index, set_count, rep_count
    time_now = rtc.datetime()
    display.fill(0)
    display.text(str(time_now[4])+ ":"+str(time_now[5])+ ":"+str(time_now[6]), 10, 10)
    display.text(str(imu.temperature())+'C',90,10)
    display.text(exercises[current_exericise_index],10,20)
    display.text('set count: '+str(set_count),10,30)
    display.text('rep count: '+str(rep_count),10,40)
    display.show()    
    
def vibrator_off(timer):
    vibrator.off()

# change type of excercise
def buttonA_callback(pin):
    print("press button detect")
    global current_exericise_index
    current_exericise_index += 1
    if current_exericise_index == 3:
        current_exericise_index = 0

i2c = machine.I2C(sda=machine.Pin(4), scl=machine.Pin(5),freq=100000)

imu = BNO055(i2c)
calibrated = False

display = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c)
display.flip(flag=True, update=True)

vibrator = Pin(14,Pin.OUT)
led = Pin(12, Pin.OUT)
sensor = HCSR04(trigger_pin=0, echo_pin=13)

exercises = ['no excercise','bench press','squat']
current_exericise_index = 0
set_count = 0
rep_count = 0
rtc = RTC()

tim0 = Timer(0)
tim0.init(period=1000, mode=Timer.PERIODIC, callback=update_display)
tim1 = Timer(1)    
button_a = Button(pin=Pin(15, mode=Pin.IN, pull=Pin.PULL_UP), callback=buttonA_callback)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect('Columbia University', '')
    while not wlan.isconnected():
        pass
ip = wlan.ifconfig()[0]
print('Connected to WIFI\nIP Adress: ' +  str(ip))


print("data initializeing...")
url = "http://3.141.152.60:5000/init"
post = requests.post(url)
post.close()

print("system start")

while True:
    
    time_now = rtc.datetime()
    time_information = str(time_now[0]) + "-" + str(time_now[1]) + "-" + str(time_now[2])
    
    # + "_" + str(time_now[4]) + ":" + str(time_now[5]) + ":" + str(time_now[6]))
      
    '''
    time_now = rtc.datetime()
    t = str(time_now[4])+ ":"+str(time_now[5])+ ":"+str(time_now[6])
    print(t)
    r = requests.post(url,data = json.dumps({"data":t}))
    r.close()    
    time.sleep(0.1)
    
    '''
    if not calibrated:
        calibrated = imu.calibrated()
 
    
        #print('Calibration required: sys {} gyro {} accel {} mag {}'.format(*imu.cal_status()))
    
       
    if current_exericise_index == 0:
        vibrator.off()
        led.off()
    else:

        jsonFile = {"time":str(time_information),"yaw":str(imu.euler()[0]),"pitch":str(imu.euler()[1]), "roll":str(imu.euler()[2]),
                    "exercise":exercises[current_exericise_index],"distance":str(int(sensor.distance_cm()))}
        jsonFile = json.dumps(jsonFile)
    
        url = "http://3.141.152.60:5000/data"
        post = requests.post(url,data = jsonFile)
        post.close()
             
        url_1 = "http://3.141.152.60:5000/result"
        response = requests.get(url_1)
        result = response.content
        result = json.loads(result.decode('utf-8'))
        response.close()
        
        print(result)
        set_count, rep_count = result['set_count'], result['rep_count']
            
        if result['unbalanced'] == 'True':
            led.on()
        else:
            led.off()
            
        if result['alarming'] == 'True':
            vibrator.on()
        else:
            vibrator.off()
            
        if result['hit'] == 'True':
            vibrator.on()
            tim1.init(period=500, mode=Timer.ONE_SHOT, callback=vibrator_off)
            
            
    time.sleep(0.01)
