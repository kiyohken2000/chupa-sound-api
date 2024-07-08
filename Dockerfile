FROM python:3.9

ENV APP_HOME /chupa_api
WORKDIR $APP_HOME

RUN apt-get update && apt-get install -y \
  cmake \
  ffmpeg \
  && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 4 --threads 8 chupa_api:app