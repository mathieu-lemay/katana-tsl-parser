lint:
    pre-commit run --all-files

test:
    uv run pytest --verbosity=1

install:
    uv sync --all-extras

update: _uv_lock install

_uv_lock:
    uv lock --upgrade
