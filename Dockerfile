ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --update --no-cache git

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

WORKDIR /src
COPY src /src

RUN pip3 install -r requirements.txt

RUN chmod a+x run.sh
CMD [ "./run.sh" ]