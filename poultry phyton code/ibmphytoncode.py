import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import json

#Provide your IBM Watson Device Credentials
organization = "hx9af7"
deviceType = "iotdevice"
deviceId = "1999"
authMethod = "token"
authToken = "123456789"


# Initialize the device client.
T=0
H=0
W=0
A=0
F=0
def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)
        if (cmd.data['command']=="lighton"):
                print("LIGHT ON IS RECEIVED")
                
        if (cmd.data['command']=="lightoff"):
                print("LIGHT OFF IS RECEIVED")
                
        if (cmd.data['command']=="fanon"):
                print("fan on")
                
        if (cmd.data['command']=="fanoff"):
                print("fan off")
        
        if cmd.command == "setInterval":
                if 'interval' not in cmd.data:
                        print("Error - command is missing required information: 'interval'")
                else:
                        interval = cmd.data['interval']
        elif cmd.command == "print":
                if 'message' not in cmd.data:
                        print("Error - command is missing required information: 'message'")
                else:
                        print(cmd.data['message'])

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        T=random.randint(-10,125)
        H=random.randint(0,100)
        W=random.randint(0,100)
        A=random.randint(0,100)
        F=random.randint(0,100)
        #Send Temperature & Humidity to IBM Watson
        data = {"d":{ 'temperature' : T, 'humidity': H, 'Water level': W, 'ammoniagas': A, 'firedetection': F}}
        print (data)
        def myOnPublishCallback():
            print ("Published Temperature = %s C" % T, "Humidity = %s %%" % H, "Water level = %s cubicfeet" %W,"Ammoniagas = %s ppm" %A ,"Firedetection = %s %%" %F,"to IBM Watson")

        success = deviceCli.publishEvent("Data", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(1)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
