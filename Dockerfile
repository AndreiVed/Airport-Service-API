FROM python:3.11.6-alpine3.18
LABEL maintrainer="vidernykov.a.e@gmail.com"

ENV PYTHOUNNBUFFERED 1

WORKDIR app/

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .
COPY entrypoint.sh /entrypoint.sh

RUN mkdir -p /files/media
RUN adduser \
    --disabled-password\
    --no-create-home \
    my_user
RUN chown -R my_user /files/media
RUN chmod -R 755 /files/media

RUN chmod +x /entrypoint.sh


USER my_user
ENTRYPOINT ["/entrypoint.sh"]

