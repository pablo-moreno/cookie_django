# {{ cookiecutter.project_name }}

![pic]({{ cookiecutter.repository_url }}/badges/master/coverage.svg)
![pic]({{ cookiecutter.repository_url }}/badges/master/pipeline.svg)


This is {{ cookiecutter.project_name }}, configured with CI/CD for testing and auto-deployment.

## :computer: Development

Run the development environment with Docker Compose

```sh
docker-compose up
```

You can create or apply migrations from the Django container:

```sh
docker exec -it <container_name> bash
python manage.py makemigrations
python manage.py migrate
```

## :cactus: Environment variables

`VERSION (string)` Application version.

`SECRET_KEY (string)` Project secret key.

`DEBUG: (TRUE|FALSE)` Whether the project is running in DEBUG mode or not. 

`DATABASE_URL (string)` Full database URL in the following format: `postgres://username:password@host:port/dbname`

`REDIS_HOST (IP|URL)` IP or URL address of the Redis instance.

`REDIS_PORT (numeric)` Port of the Redis instance.

`PAGE_SIZE (numeric)` Number of items to paginate by default in the API responses.

## :hammer_and_wrench: Build project

You can build the project image running:

```sh
docker build -t {{ cookiecutter.project_slug }}:<version> .
```

## :rocket: Run built project

To run the built project you can run this command:

```sh
docker run -d \
    -p 8000:8000 \
    -v /var/www/{{ cookiecutter.project_slug }}/static:/app/static \
    -v /var/www/{{ cookiecutter.project_slug }}/media:/app/media \
    -e <environment variable name>=<value> \
    -e DEBUG=FALSE \
    {{ cookiecutter.project_slug }}:<version>
```

You must setup as much environment variables as you need.


## :gear: Gitlab Environment Variables

Setup CI/CD variables on Settings > CI / CD > Variables.

```sh
CI_PROJECT_BASE_IMAGE=<project base image name>
CI_PROJECT_NAME=<project name>

CI_POSTGRES_DATABASE=<my internal postgres database name>
CI_POSTGRES_PASSWORD=<postgres password>
CI_POSTGRES_USER=<postgres password>

CI_DOCKER_REGISTRY=<my.docker.registry.domain>
CI_REGISTRY_USER=<docker registry user>
CI_REGISTRY_PASSWORD=<docker registry password>
```
