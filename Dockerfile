FROM python:3.9.12-bullseye
WORKDIR /app
RUN pip install django djangorestframework
RUN pip install pycrypto mysqlclient
COPY . /app

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

ENTRYPOINT ["dockerize", "-wait", "tcp://routine_db:3306", "-timeout", "30s"]

RUN python manage.py makemigrations
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8003" ]
EXPOSE 8000