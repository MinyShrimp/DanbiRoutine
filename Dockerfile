FROM python:3.9.12-bullseye
WORKDIR /app
RUN pip install django djangorestframework
RUN pip install pycrypto mysqlclient
COPY . /app
RUN python manage.py makemigrations
CMD [ "python", "manage.py", "runserver" ]
EXPOSE 8003