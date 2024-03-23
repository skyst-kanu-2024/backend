FROM python:3.11

WORKDIR /app

RUN pip install -U pip wheel setuptools
RUN pip install gunicorn

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD . .

CMD [ "gunicorn", "app:app", "-b", "0.0.0.0:5000", "--log-level", "info", "-w", "2", "--threads", "2", "--worker-class", "gthread"]
