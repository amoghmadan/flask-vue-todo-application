FROM python:3.10-slim-bullseye

WORKDIR /tracker

RUN python3 -m pip install gunicorn poetry

COPY ./pyproject.toml ./poetry.lock /tracker/

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi
