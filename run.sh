#!/usr/bin/with-contenv bashio

export MQTT_HOST="$(bashio::services mqtt 'host')"
export MQTT_PORT="$(bashio::services mqtt 'port')"
export MQTT_USER="$(bashio::services mqtt 'username')"
export MQTT_PASSWD="$(bashio::services mqtt 'password')"

if  bashio::config.has_value 'mqtt_host'; then export MQTT_HOST="$(bashio::config 'mqtt_host')"; fi
if  bashio::config.has_value 'mqtt_user'; then export MQTT_USER="$(bashio::config 'mqtt_user')"; fi
if  bashio::config.has_value 'mqtt_passwd'; then export MQTT_PASSWD="$(bashio::config 'mqtt_passwd')"; fi

export RFXTRX_HOST="$(bashio::config 'rfxtrx_host')"
export RFXTRX_PORT="$(bashio::config 'rfxtrx_port')"

echo MQTT_HOST=$MQTT_HOST
echo MQTT_PORT=$MQTT_PORT
echo MQTT_USER=$MQTT_USER
echo RFXTRX_HOST=$RFXTRX_HOST
echo RFXTRX_PORT=$RFXTRX_PORT

python3 -u rfxtrx-mqtt.py
