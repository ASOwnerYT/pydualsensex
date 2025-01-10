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

def set_trigger(trigger: DSTrigger, params):
    match params[3]:
        case 1:
            trigger.setMode(TriggerModes.Rigid)
        case 12:
            trigger.setMode(TriggerModes.Pulse_AB) # close enough

    for param_id in range(4, 11):
        # Force parameters start from the 4th index of the parameter array. There can only be 7 parameters.
        paramID = param_id - 4
        trigger.setForce(paramID, int(params[param_id]))

while True:
    # Get parsed data
    data = json.loads(sock.recv(1024).decode('utf-8'))
    print(data)

    for i in data['instructions']:
        match i['type']:
            case 1:
                # Set trigger modes
                match i['parameters'][1]:
                    case 1:
                        set_trigger(dualsense.triggerL, i['parameters'])
                    case 2:
                        set_trigger(dualsense.triggerR, i['parameters'])

            case 2:
                dualsense.light.setColorI(i['parameters'][1], i['parameters'][2], i['parameters'][3])
            case 3:
                leds = None
                for index in range(1, 6):
                    if i['parameters'][index]:
                        match index:
                            case 1:
                                leds = PlayerID.PLAYER_1
                            case 2:
                                leds = PlayerID.PLAYER_2
                            case 3:
                                leds = PlayerID.PLAYER_3
                            case 4:
                                leds = PlayerID.PLAYER_4
                            case 5:
                                leds = PlayerID.ALL
                        if leds:
                            dualsense.light.setPlayerID(leds)
