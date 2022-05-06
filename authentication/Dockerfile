FROM python:3.7

RUN apt update
RUN pip3 install --upgrade pip
RUN mkdir /project
WORKDIR /project
COPY requirements.txt requirements.txt


RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 8080

# CMD flask run
CMD python run.py