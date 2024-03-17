FROM python:3.12.2-slim

# Configure Poetry
ENV POETRY_VERSION=1.8.2
ENV POETRY_VENV=/opt/poetry-venv

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
	&& $POETRY_VENV/bin/pip install -U pip setuptools \
	&& $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /Flask-app

# Install dependencies
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.in-project true \
    && poetry env use python \
    && poetry install --no-dev

# Run your app
COPY . .
CMD ["poetry", "run", "flask", "--app","app.main","run","--host=0.0.0.0"]
