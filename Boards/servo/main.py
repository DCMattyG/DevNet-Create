import machine
import time
import json
from umqtt.simple import MQTTClient

# Format:
# {
#     "command":    "<left/right/center/wave>",
# }

waiting = 1
command = ""

def servoLoop():
    global waiting
    global command
    global servo

    while True:
        while(waiting):
            client.check_msg()
            time.sleep(1)
    
        print("Command:", command)

        if(command == "left"):
            waiting = 1
            servo.duty(115)
        elif(command == "right"):
            waiting = 1
            servo.duty(35)
        elif(command == "center"):
            waiting = 1
            servo.duty(75)
        elif(command == "wave"):
            waiting = 1
            waveServo()
        else:
            waiting = 1
            command = ""

def servo_cb(topic, msg):
    global waiting
    global command

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

def waveServo():
    global servo

    while(waiting):
        servo.duty(35)
        time.sleep(1)
        servo.duty(115)
        time.sleep(1)
        client.check_msg()

servo = machine.PWM(machine.Pin(4), freq=50)
servo.duty(75)
time.sleep(5)
client = MQTTClient(client_id="ESP8266-SERVO", server="192.168.50.10")
client.set_callback(servo_cb)
client.connect()
client.subscribe(b"servo")
servoLoop()