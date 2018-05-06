FROM python:3

WORKDIR /usr/src/app

RUN pip install --no-cache-dir speedtest-cli schedule

COPY . .

CMD [ "python", "./run.py" ]
