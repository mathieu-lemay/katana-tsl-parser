DOCKER_IMAGE := "katana-tsl-parser"
DOCKER_TAG := "dev"

lint:
    pre-commit run --all-files

test:
    poetry run pytest \
        --cov --cov-append --cov-report term-missing --cov-fail-under=100 \
        --verbosity=1

install:
    poetry install --sync

update: _poetry_lock install

docker-build:
    docker build --tag "{{ DOCKER_IMAGE }}:{{ DOCKER_TAG }}" .

_poetry_lock:
    poetry update --lock
