FROM python:3.7-stretch

# create application directory
WORKDIR ~
RUN mkdir app
WORKDIR app

# copy and install environment as soon as possible
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy executables
COPY src/flask src/flask
COPY tests tests

ENTRYPOINT ["gunicorn", "-b", ":8080","src.flask.main:APP"]

