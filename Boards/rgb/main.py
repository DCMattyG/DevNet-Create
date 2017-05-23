import machine
import time
import json
from umqtt.simple import MQTTClient

# Format:
# {
#     "color":      "(<r>, <g>, <b>)"
# }

waiting = 1
color = []

def rgbLoop():
    global waiting
    global color

    while True:
        while(waiting):
            client.check_msg()
            time.sleep(1)
    
        print("Color:", color)
        setRGB()
        color = []

def rgb_cb(topic, msg):
    global waiting
    global color

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
        tempColor = jTemp['color']
        tempColor = tempColor.replace("(","")
        tempColor = tempColor.replace(")","")
        colorList = tempColor.split(',')
        color.append(int(colorList[0]))
        color.append(int(colorList[1]))
        color.append(int(colorList[2]))
    except:
        color = []
        waiting = 1
        return
        pass

def setRGB():
    global r
    global g
    global b
    global waiting

    r.duty(1025-(color[0]*4))
    g.duty(1025-(color[1]*4))
    b.duty(1025-(color[2]*4))

    waiting = 1

r = machine.PWM(machine.Pin(5), freq=1000)
g = machine.PWM(machine.Pin(4), freq=1000)
b = machine.PWM(machine.Pin(14), freq=1000)
r.duty(1500)
g.duty(1500)
b.duty(1500)
time.sleep(5)
client = MQTTClient(client_id="ESP8266-RGB", server="192.168.50.10")
client.set_callback(rgb_cb)
client.connect()
client.subscribe(b"rgb")
rgbLoop()