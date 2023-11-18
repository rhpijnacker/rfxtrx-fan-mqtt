#!/usr/bin/python

from RFXtrx import PyNetworkTransport, FanDevice
from RFXtrx.lowlevel import Fan
import paho.mqtt.client as mqtt
import logging
import traceback
import sys

from datetime import datetime
from settings import *

logging.basicConfig(level=logging.DEBUG)

def on_connect(client, userdata, flags, rc):
    client.subscribe("rfxtrx/#", 0)

def on_message(client, userdata, msg):
    try:
        print(timestamp() + "\tRECIEVED MQTT MESSAGE: " + msg.topic + " " + str(msg.payload))

        parts = msg.topic.split("/")
        if parts[-1] != "set":
            return

        print(f"payload = {msg.payload}")
        if parts[-2] == "percentage":
            pct, pr, stat, cmd = convert_pct(int(msg.payload))
        elif parts[-2] == "preset":
            pct, pr, stat, cmd = convert_preset(str(msg.payload))
        else:
            pct, pr, stat, cmd = convert_onoff(msg.payload.decode())

        print(f"{pct}, {pr}, {stat}, {cmd}")

        send_rfxtrx_command(cmd)
        send_mqtt_state(pct, pr, stat)

    except Exception as e:
        print(e)
        traceback.print_exc()
        print("Error when parsing incomming message.")

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%s")

def convert_pct(value):
    if value == 0:
        return 0, 'low', 'OFF', Fan.Commands.LOW.value
    elif value == 1:
        return 1, 'medium', 'ON', Fan.Commands.MEDIUM.value
    else:
        return 2, 'high', 'ON', Fan.Commands.HIGH.value

def convert_preset(value):
    if value == 'low':
        return 0, 'low', 'OFF', Fan.Commands.LOW.value
    elif value == 'medium':
        return 1, 'medium', 'ON', Fan.Commands.MEDIUM.value
    else:
        return 2, 'high', 'ON', Fan.Commands.HIGH.value

def convert_onoff(value):
    if value == "OFF":
        return 0, 'low', 'OFF', Fan.Commands.LOW.value
    else:
        return 2, 'high', 'ON', Fan.Commands.HIGH.value

def convert_cmnd(value):
    if value == 'Low':
        return 0, 'low', 'OFF'
    elif value == 'Medium':
        return 1, 'medium', 'ON'
    elif value == 'High':
        return 2, 'high', 'ON'
    else:
        return None, None, None

def send_rfxtrx_command(cmd):
    pkt = Fan()
    pkt.packettype = 0x17
    pkt.set_transmit(
        Fan.Types.ITHO_RFT.value,
        0x74ea6d,
        cmd
    )
    print(transport)
    try:
        transport.send(pkt.data)
    except BrokenPipeError:
        print(timestamp() + "\tBrokenPipeError, exiting")
        sys.exit()

def send_mqtt_state(pct, preset, onoff):
    print(f"Publish {pct}, {preset}, {onoff}")
    client.publish("rfxtrx/fan/74ea6d/state", onoff, retain=True)
    client.publish("rfxtrx/fan/74ea6d/percentage/state", pct, retain=True)
    client.publish("rfxtrx/fan/74ea6d/preset/state", preset, retain=True)


client = mqtt.Client("rfxtrx-fan-mqtt")
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(MQTT_USER, MQTT_PASSWD)

client.connect(MQTT_HOST)
config_payload = '''{
    "name": "rfxtrx_74ea6d",
    "unique_id": "rfxtrx_74ea6d",
    "enabled_by_default": "true",
    "device": {
        "identifiers": ["RFXtrx-mqtt"],
        "name": "RFXtrx 74ea6d"
    },
    "~": "rfxtrx/fan/74ea6d",
    "cmd_t": "~/set",
    "pct_cmd_t": "~/percentage/set",
    "pct_stat_t": "~/percentage/state",
    "pr_mode_cmd_t": "~/preset/set",
    "pr_mode_stat_t": "~/preset/state",
    "pr_modes": ["low", "medium", "high"],
    "speed_range_min": 1,
    "speed_range_max": 2,
    "stat_t": "~/state"
}'''
client.publish("homeassistant/fan/rfxtrx_74ea6d/config", payload=config_payload, qos=1, retain=True)

client.loop_start()

transport = PyNetworkTransport((RFXTRX_HOST, RFXTRX_PORT))
transport.reset()

while True:
    event = transport.receive_blocking()
    if event == None or not isinstance(event.device, FanDevice):
        continue

    print(timestamp() + "\t" + str(event))

    pct, pr, stat = convert_cmnd(str(event.values['Command']))
    print(pct, pr, stat)
    if stat is not None:
        send_mqtt_state(pct, pr, stat)