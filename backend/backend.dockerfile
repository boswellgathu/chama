FROM python:3.10.4-slim-buster

COPY ./start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh
WORKDIR /backend/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN set -eux; \
    apt-get update -q -y --force-yes; \
    apt-get install gcc -q -y; \
    apt-get install curl libpq-dev -q -y --force-yes

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /backend/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN file="$(ls -la)" && echo $file
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.custom_display_url=http://127.0.0.1:8888
ARG INSTALL_JUPYTER=false
RUN bash -c "if [ $INSTALL_JUPYTER == 'true' ] ; then pip install jupyterlab ; fi"

COPY . /backend
ENV PYTHONPATH=/backend

