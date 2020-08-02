FROM {{ cookiecutter.base_docker_image }}

WORKDIR /app
COPY . /app

ARG VERSION
ENV APP_VERSION=$VERSION

RUN poetry install
RUN poetry run manage.py collectstatic --noinput
