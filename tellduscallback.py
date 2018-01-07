from ctypes import c_int, c_ubyte, c_void_p, POINTER, string_at #imports allowing the use of our library
from threading import Timer
from datetime import datetime
import time
import platform
import socket

#platform specific imports:
if (platform.system() == 'Windows'):
	#Windows
	from ctypes import windll, WINFUNCTYPE
	lib = windll.LoadLibrary('TelldusCore.dll') #import our library
else:
	#Linux
	from ctypes import cdll, CFUNCTYPE
	lib = cdll.LoadLibrary('libtelldus-core.so.2') #import our library

timers = {} #timerlist

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
	
	#lib.tdTurnOff(1)
	
#function to be called when a device event occurs		
def callbackfunction(deviceId, method, value, callbackId, context):
	global timers
	
	print "callback!"
	f= open('/home/pi/tellduslog', 'a')
	if (method == 1):
		f.write("D_on: " + str(deviceId) + datetime.now().strftime(' %Y-%m-%d %H:%M:%S') + "\n"  )
	else:
		f.write("D_off: " + str(deviceId) + datetime.now().strftime(' %Y-%m-%d %H:%M:%S') + "\n"  )
	f.close()


	if (deviceId == 1):
		# is turning on deviceId 1 here, so just return if events for that device are picked up
		return
		
	t = 0
	print "Received event for device %d" % (deviceId,)
	if (deviceId in timers):
		# a timer already exists for this device, it might be running so interrupt it
		# Many devices (for example motion detectors) resends their messages many times to ensure that they
		# are received correctly. In this example, we don't want to run the turnOn/turnOff methods every time, instead we
		# start a timer, and run the method when the timer is finished. For every incoming event on this device, the timer
		# is restarted.
		t = timers[deviceId] 
		t.cancel()
	if (method == 1):
		if(deviceId == 21):
			#on
			t = Timer(0.5, turnOn) #start timer with 0.5 second delay (adjust the delay to suit your needs), then turn on
	else:
		if(deviceId == 21):		#off
			t = Timer(00.5, turnOff) #start timer with 0.5 second delay (adjust the delay to suit your needs), then turn off

	t.start()
	timers[deviceId] = t #put timer in list, to allow later cancellation

#function to be called when device event occurs, even for unregistered devices
def rawcallbackfunction(data, controllerId, callbackId, context):
	print string_at(data)

if (platform.system() == 'Windows'):
	CMPFUNC = WINFUNCTYPE(None, c_int, c_int, POINTER(c_ubyte), c_int, c_void_p) #first is return type
	CMPFUNCRAW = WINFUNCTYPE(None, POINTER(c_ubyte), c_int, c_int, c_void_p)
else:
	CMPFUNC = CFUNCTYPE(None, c_int, c_int, POINTER(c_ubyte), c_int, c_void_p)
	CMPFUNCRAW = CFUNCTYPE(None, POINTER(c_ubyte), c_int, c_int, c_void_p)

cmp_func = CMPFUNC(callbackfunction)
cmp_funcraw = CMPFUNCRAW(rawcallbackfunction)

lib.tdInit()
lib.tdRegisterDeviceEvent(cmp_func, 0)
#lib.tdRegisterRawDeviceEvent(cmp_funcraw, 0) #uncomment this, and comment out tdRegisterDeviceEvent, to see data for not registered devices

print "Waiting for events..."
while(1):
	time.sleep(0.5) #don't exit
