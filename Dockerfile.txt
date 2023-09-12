FROM python:slim

RUN useradd todo

WORKDIR /home/todo

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY microblog.py config.py boot.sh ./
COPY wsgi.py wsgi.py
RUN chmod +x boot.sh

ENV FLASK_APP microblog.py

RUN chown -R todo:todo ./
USER todo

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]