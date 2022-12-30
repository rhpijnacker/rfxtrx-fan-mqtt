ARG BUILD_FROM
FROM $BUILD_FROM

WORKDIR /src
COPY src /src

RUN pip install -r

CMD [ "python", "rfxtrx-mqtt.py" ]