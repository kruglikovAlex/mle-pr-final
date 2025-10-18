FROM python:3.11-slim
LABEL author=${LABEL}


COPY . /mlflow_server
WORKDIR mlflow_server

RUN pip3 install -r requirements.txt

EXPOSE 5000

#RUN set -ex && apk --no-cache add sudo
#RUN chmod +x run_mlflow_registry.sh
CMD ./run_mlflow_registry.sh
