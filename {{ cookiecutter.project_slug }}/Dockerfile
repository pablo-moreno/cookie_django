FROM registry.gitlab.com/pablo-moreno/geopython:latest

WORKDIR /app
COPY . /app

ARG VERSION

ENV DJANGO_SETTINGS_MODULE=config.settings.production
ENV APP_VERSION=$VERSION

RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput
