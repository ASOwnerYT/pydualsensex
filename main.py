import json
from socket import *
from pydualsense import *

# get dualsense instance
dualsense = pydualsense()
dualsense.init()

# Create a UDP socket
sock = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to socket
sock.bind(('127.0.0.1', 6969))

while True:
    # Get parsed data
    data = json.loads(sock.recv(1024).decode('utf-8'))
    print(data)

    # Set trigger modes
    match data["instructions"][0]["parameters"][3]:
        case 1:
            dualsense.triggerL.setMode(TriggerModes.Rigid)
        case 12:
            dualsense.triggerL.setMode(TriggerModes.Pulse_AB) # close enough

    match data["instructions"][1]["parameters"][3]:
        case 1:
            dualsense.triggerR.setMode(TriggerModes.Rigid)
        case 12:
            dualsense.triggerR.setMode(TriggerModes.Pulse_AB) # close enough

    # Set force parameters
    for id in range(4, 11):
        # Force parameters start from the 4th index of the parameter array. There can only be 7 parameters.
        paramID = id - 4

        # Set left trigger parameter value
        dualsense.triggerL.setForce(paramID, int(data["instructions"][0]["parameters"][id]))

        # Set right trigger parameter value
        dualsense.triggerR.setForce(paramID, int(data["instructions"][1]["parameters"][id]))
