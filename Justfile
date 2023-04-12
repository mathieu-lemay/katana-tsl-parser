DOCKER_IMAGE := "katana-tsl-parser"
DOCKER_TAG := "dev"

install:
    poetry install --sync

update: _poetry_lock install

lint:
    pre-commit run --all-files

test:
    poetry run pytest --verbosity=1

docker-build:
    docker build --tag "{{ DOCKER_IMAGE }}:{{ DOCKER_TAG }}" .

_poetry_lock:
    poetry update --lock
