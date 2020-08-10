FROM python:slim-buster

ADD . /usr/src/shakawiki
WORKDIR /usr/src/shakawiki/shakawiki/

RUN cd /usr/src/shakawiki/ && \
        pip install pipenv && \
        pipenv install

RUN pipenv run python manage.py setup && \
        pipenv run python manage.py migrate

CMD pipenv run python manage.py runserver 0.0.0.0:8000
