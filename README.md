# Telldus-Callback-with-UDP
This is a variation on the Telldus callback.py script. 
https://github.com/telldus/telldus/blob/master/examples/python/callbacks.py

The script provides two features

Logging of Telldus events to a logfile

Sending UDP Packets to a a host for a specific event.

Used togeter with the Homebridge plugin
https://www.npmjs.com/package/homebridge-udp-contactsensor

It provides a way to represent a telldus device as a Contact sensor i Apple home application. 
This provides a method to generate Noificationsin the Appple device based on Telldus events.

# Configuration

IN the on and of sections oh the callback script IP adress, UDP Port and Message must match...
```
def turnOn():
	print "turning on"
	UDP_IP = "127.0.0.1"
	UDP_PORT = 8266
	MESSAGE = "open"	
	sock = socket.socket(socket.AF_INET, # Internet
    socket.SOCK_DGRAM) # UDP
	sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
	#lib.tdTurnOn(1)
  
  def turnOff():
	print "turning off"
	UDP_IP = "127.0.0.1"
	UDP_PORT = 8266
	MESSAGE = "close"	
	sock = socket.socket(socket.AF_INET, # Internet
    socket.SOCK_DGRAM) # UDP
	sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
```
  ... The section in config.json 
```
{
            "accessory": "UdpContactSensor",
            "name": "UDP Contact Sensors",
            "listen_port": 8266,
            "data": {
                "Switch #2": { "on": "6f70656e", "off": "636c6f7365" },
                "Switch #3": { "on": "03ff", "off": "0300" },
                "Switch #4": { "on": "04ff", "off": "0400" }
            }
        },
```
deviceId matches a device ID entry in tellstick.conf  
```
	if (method == 1):
		if(deviceId == 21):
			#on
			t = Timer(0.5, turnOn) #start timer with 0.5 second delay (adjust the delay to suit your needs), then turn on
	else:
		if(deviceId == 21):		#off
			t = Timer(00.5, turnOff) #start timer with 0.5 second delay (adjust the delay to suit your needs), then turn off
  
```



