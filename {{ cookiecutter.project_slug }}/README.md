# {{ cookiecutter.project_name }}

This is {{ cookiecutter.project_name }}, configured with CI/CD for testing and auto-deployment.

## Development

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


## Gitlab Environment Variables

Setup CI/CD variables on Settings > CI / CD > Variables.


```sh
CI_PROJECT_BASE_IMAGE=<project base image name>
CI_PROJECT_NAME=<project name>

CI_POSTGRES_DATABASE=<my internal postgres database name>
CI_POSTGRES_PASSWORD=<postgres password>
CI_POSTGRES_USER=<postgres password *>

CI_DOCKER_REGISTRY=<my.docker.registry.domain>
CI_REGISTRY_USER=<docker registry user*>
CI_REGISTRY_PASSWORD=<docker registry password *>
```

Those marked with asterisk (*) require to be masked and protected.

To do so, just run the command:

`echo -n <variable_value> | base64`
