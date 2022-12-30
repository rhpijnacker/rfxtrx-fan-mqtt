#!/usr/bin/with-contenv bashio

export MQTT_HOST="$(bashio::services mqtt 'host')"
export MQTT_PORT="$(bashio::services mqtt 'port')"
export MQTT_USER="$(bashio::services mqtt 'username')"
export MQTT_PASSWD="$(bashio::services mqtt 'password')"

export RFXTRX_HOST=192.168.2.247
export RFXTRX_PORT=10001

#if  bashio::config.has_value 'mqtt_host'; then export MQTT_HOST="$(bashio::config 'mqtt_host')"; fi
#if  bashio::config.has_value 'mqtt_user'; then export MQTT_USER="$(bashio::config 'mqtt_user')"; fi
#if  bashio::config.has_value 'mqtt_passwd'; then export MQTT_PASSWD="$(bashio::config 'mqtt_passwd')"; fi

if  bashio::config.has_value 'rfxtrx_host'; then export RFXTRX_HOST="$(bashio::config 'rfxtrx_host')"; fi
if  bashio::config.has_value 'rfxtrx_passwd'; then export RFXTRX_PORT="$(bashio::config 'rfxtrx_passwd')"; fi

env

python3 -u rfxtrx-mqtt.py
