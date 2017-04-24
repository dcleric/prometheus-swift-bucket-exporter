FROM alpine:3.4

MAINTAINER 2gis-io <io@2gis.ru>

ADD . /tmp/prometheus-swift-bucket

WORKDIR /tmp/prometheus-swift-bucket/

RUN apk add --no-cache --update python py-pip && pip install -r /tmp/prometheus-swift-bucket/requirements.txt

CMD ["python", "swift-prom.py"]
