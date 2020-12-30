FROM python:3.7.2-slim
WORKDIR ~

# copy and install environment as soon as possible
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy executables
COPY src/flask src/flask
COPY tests tests

ENTRYPOINT ["python", "src/flask/main.py"]

