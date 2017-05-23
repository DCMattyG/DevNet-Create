import machine
import time
import neopixel
import json
from umqtt.simple import MQTTClient

# Format:
# {
#     "command":    "one",
#     "pixelNum":   <0-11>,
#     "color":      "(<r>, <g>, <b>)"
# }
#
# {
#     "command": "loop"
# }

waiting = 1
command = ""
pixelNum = 0
color = []

def neoLoop(np):
    global waiting
    global command
    global pixelNum
    global color

    while True:
        while(waiting):
            client.check_msg()
            time.sleep(1)
    
        print("Command:", command)
        print("pixelNum:", pixelNum)
        print("Color:", color)

        if(command == "loop"):
            waiting = 1
            colorLoop(np)
        elif(command == "one"):
            waiting = 1
            showPixel(np, pixelNum, color)
            command = ""
            pixelNum = 0
            color = []
        else:
            waiting = 1
            command = ""
            pixelNum = 0
            color = []

def neo_cb(topic, msg):
    global waiting
    global command
    global pixelNum
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
        command = jTemp['command']
    except:
        waiting = 1
        return
        pass

    if(command == "one"):
        try:
            pixelNum = jTemp['pixelNum']
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
            waiting = 1
            return
            pass
    elif(command != "loop"):
        waiting = 1

def createPixel(gpio, pixels):
    pin = machine.Pin(gpio, machine.Pin.OUT)
    np = neopixel.NeoPixel(pin, pixels)
    return np

def showPixel(np, pixelNum, color):
    rgb = [0, 0, 0]
    clearPixels(np)
    
    try:
        if(pixelNum > 11):
            pixelNum = 11
        elif(pixelNum < 0):
            pixelNum = 1
    except:
        waiting = 1
        return
        pass

    print("Show Color:", color)
    print("Color Type", type(color))

    for i in range (0, 3):
        if(color[i] > 255):
            rgb[i] = 255
        elif(color[i] < 0):
            rgb[i] = 0
        else:
            rgb[i] = int(color[i])

    newColor = (rgb[0], rgb[1], rgb[2])
    #print("newColor:", newColor)
    np[pixelNum] = newColor
    np.write()

def clearPixels(np):
    pixels = np.n
    off = (0, 0, 0)
    
    for x in range (0, pixels):
        np[x] = off
        np.write()

def rotateColor(np, color, pos, delay):
    pixels = np.n
    off = (0, 0, 0)

    for x in range (pos, (pos + (pixels - 3))):
        newpos = (x % pixels)
        np[(x % pixels)] = color
        np[((x - 1) % pixels)] = off
        np.write()
        time.sleep_ms(delay)
    return ((newpos + 1) % pixels)

def colorLoop(np):
    pixels = np.n
    delay = 100
    off = (0, 0, 0)
    red = (255, 0, 0)
    blue = (0, 255, 0)
    green = (0, 0, 255)

    redpos = 2
    greenpos = 1
    bluepos = 0

    clearPixels(np)

    while(waiting):
        redpos = rotateColor(np, red, redpos, delay)
        greenpos = rotateColor(np, green, greenpos, delay)
        bluepos = rotateColor(np, blue, bluepos, delay)
        client.check_msg()

numPixels = 12
gpioPin = 5
neo = createPixel(gpioPin, numPixels)
time.sleep(5)
client = MQTTClient(client_id="ESP8266-NEO", server="192.168.50.10")
client.set_callback(neo_cb)
client.connect()
client.subscribe(b"neo")
neoLoop(neo)