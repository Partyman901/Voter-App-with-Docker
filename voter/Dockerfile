FROM python:3.8-slim-buster
RUN apt update
RUN pip3 install --upgrade pip
RUN mkdir /app
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 8110
CMD python run.py