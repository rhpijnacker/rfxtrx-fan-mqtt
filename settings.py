import os

MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWD = os.getenv("MQTT_PASSWD")

RFXTRX_HOST = os.getenv("RFXTRX_HOST")
RFXTRX_PORT = int(os.getenv("RFXTRX_PORT"))