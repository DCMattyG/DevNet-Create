import machine
import time
import json
import ntptime
from ssd1306 import SSD1306_I2C
from umqtt.simple import MQTTClient

# Format:
# {
#     "command":    "text",
#     "text":       "<string>
# }
#
# {
#     "command": "<date/time>"
# }

waiting = 1
command = ""
text = ""

def lcdLoop():
    global waiting
    global command
    global text

    while True:
        while(waiting):
            client.check_msg()
            time.sleep(1)
    
        waiting = 1

def lcd_cb(topic, msg):
    global waiting
    global command
    global text
    global oled

    waiting = 0
    print((topic, msg))
    result = msg.decode("utf-8") #convert to string
    try:
        jTemp = json.loads(result)
    except:
        waiting = 1
        return
        pass

    try:
        command = jTemp['command']
    except:
        waiting = 1
        return
        pass

    if(command == "text"):
        try:
            text = jTemp['text']
            oled.fill(0)
            oled.text(text, 0, 0)
            oled.show()
        except:
            waiting = 1
            return
            pass
    elif(command == "date"):
        try:
            ntptime.settime()
            year, month, day, hour, minute, second, ms, dayinyear = time.localtime()
            text = str(month) + "/" + str(day) + "/" + str(year)
            oled.fill(0)
            oled.text(text, 0, 0)
            oled.show()
        except:
            waiting = 1
            return
            pass
    elif(command == "time"):
        try:
            ntptime.settime()
            year, month, day, hour, minute, second, ms, dayinyear = time.localtime()
            text = str(hour) + ":" + str(minute) + ":" + str(second)
            oled.fill(0)
            oled.text(text, 0, 0)
            oled.show()
        except:
            waiting = 1
            return
            pass

i2c = machine.I2C(scl = machine.Pin(5), sda = machine.Pin(4))
oled = SSD1306_I2C(128, 64, i2c)
time.sleep(5)
client = MQTTClient(client_id="ESP8266-LCD", server="192.168.50.10")
client.set_callback(lcd_cb)
client.connect()
client.subscribe(b"lcd")
lcdLoop()