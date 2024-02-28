FROM python:3.12.2-slim
WORKDIR /app
RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY pyproject.toml .
COPY JastieDatabase /app/JastieDatabase
RUN poetry install --with test
LABEL authors="halone"


ENTRYPOINT ["poetry", "run", "prod"]