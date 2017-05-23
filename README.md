IoT Lab Instructions

Notes:
·	The wireless connection is:
o	SSID: devnetcreate
o	PASS: devnetcreate
·	Your IP address is 192.168.50.X, where “X” is <Your Device Number> + 30.
·	Your client ID is “ESP8266” + Your Name (e.g. ESP8266-MATT)
·	Use the code block below to test various IoT devices.
·	In MicroPython, you can press CTRL+D for a soft reset – You will need to reconnect WebREPL afterwards.

MQTT Publisher Code Block:

from umqtt.simple import MQTTClient

client = MQTTClient(client_id=”ESP8266-<NAME>”, server=“192.168.50.10”, port=8883, ssl=True)
client.connect()

client.publish(‘<topic>’, ‘<message>’)

Available Topics:
“neo”
{
    “command”: “<one/loop>”,
    “pixelNum”: <0-11>,
    “color”: “(<0-255>, <0-255>, <0-255>”
}

“lcd”
{
    “command”: “<text/date/time>”,
    “text”: “<text>”
}


“rgb”
{
    “color”: “(<0-255>, <0-255>, <0-255>)”
}

“servo”
{
    “command”: “<left/right/center/wave>”
}

Examples:
Neopixel Loop Show:
{
    “command”: “loop”
}

NeoPixel Pixel #5 Blue:
{
    “command”: “one”,
    “pixelNum”: 5,
    “color”: “(0, 0, 255)”
}

LCD Custom Text:
{
    “command”: “text”,
    “text”: “Hello!”
}


LCD Show Time:
{
    “command”: “time”
}

RGB LED Green:
{
    “color”: “(0,255,0)”
}

Servo Wave Show:
{
    “command”: “wave”
}

Servo Arm Center:
{
    “command”: “center”
}
