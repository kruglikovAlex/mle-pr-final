FROM python:3.11-slim
LABEL author=${LABEL}

COPY . ./ml_service
WORKDIR ml_service

RUN pip3 install -r requirements.txt

EXPOSE 8081 8082 8088
