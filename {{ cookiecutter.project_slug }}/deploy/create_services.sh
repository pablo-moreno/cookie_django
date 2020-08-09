#!/bin/bash

# Create private network
docker network create -d overlay {{ cookiecutter.project_slug }}

# Create volumes mapped to the specified directories
docker volume create {{ cookiecutter.project_slug }}_db -d local-persist -o mountpoint=/var/www/{{ cookiecutter.project_slug }}/db
docker volume create {{ cookiecutter.project_slug }}_static -d local-persist -o mountpoint=/var/www/{{ cookiecutter.project_slug }}/static
docker volume create {{ cookiecutter.project_slug }}_media -d local-persist -o mountpoint=/var/www/{{ cookiecutter.project_slug }}/media

# POSTGRES service
docker service create \
  --name {{ cookiecutter.project_slug }}_postgres \
  --replicas 1 \
  --env "POSTGRES_USER=${PROJECT_DB_USER}" \
  --env "POSTGRES_PASSWORD=${PROJECT_DB_PASSWORD}" \
  --env "POSTGRES_DB={{ cookiecutter.project_slug }}_backend" \
  --mount src={{ cookiecutter.project_slug }}_db,dst=/var/lib/postgresql/data \
  --network {{ cookiecutter.project_slug }} \
  postgres:latest


# REDIS service
docker service create \
  --name {{ cookiecutter.project_slug }}_redis \
  --replicas 1 \
  --mount src={{ cookiecutter.project_slug }}_db,dst=/var/lib/postgresql/data \
  --network {{ cookiecutter.project_slug }} \
  redis:latest


# BACKEND service
docker service create \
  --name {{ cookiecutter.project_slug }}_backend \
  --replicas 3 \
  --env "DATABASE_URL=postgres://$PROJECT_DB_USER:$PROJECT_DB_PASSWORD@{{ cookiecutter.project_slug }}_postgres:5432/{{ cookiecutter.project_slug }}_backend" \
  --publish "8000:8000" \
  --network {{ cookiecutter.project_slug }} \
  --mount src={{ cookiecutter.project_slug }}_media,dst=/app/media \
  --mount src={{ cookiecutter.project_slug }}_static,dst=/app/static \
  --entrypoint "./runserver.sh" \
  --with-registry-auth \
  registry.gitlab.com/pablo-moreno/{{ cookiecutter.project_slug }}-back:latest
