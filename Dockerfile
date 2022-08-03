# Pull base image
FROM python:3.10-buster as builder

# Copy requirements.txt
COPY requirements.txt requirements.txt

# Install pipenv
RUN set -ex && pip install --upgrade pip

# Install dependencies
RUN set -ex && pip install -r requirements.txt

FROM builder as final
WORKDIR /source
COPY ./app /source/
