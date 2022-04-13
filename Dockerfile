FROM python:3.9.12-bullseye
WORKDIR /app
COPY . /app

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# ENTRYPOINT ["dockerize", "-wait", "tcp://routine_db:3306", "-timeout", "30s"]

RUN dockerize -wait tcp://routine_db:3306 -timeout 30s

RUN pip install Django djangorestframework djangorestframework-simplejwt mysqlclient django-cors-headers
RUN pip install pyJWT==1.7.1

RUN apt-get update
RUN apt-get install tzdata
RUN export TZ=Asia/Seoul

RUN python manage.py makemigrations
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8003" ]
EXPOSE 8003