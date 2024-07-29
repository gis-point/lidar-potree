FROM python:3.10.12

# `DJANGO_ENV` arg is used to make prod / dev builds:
ARG DEPLOY \
  # Needed for fixing permissions of files created by Docker:
  UID=1000 \
  GID=1000

ENV DEPLOY=${DEPLOY} \
  # project working directory
  APP_PATH='/usr/src/potree_backend' \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_ROOT_USER_ACTION=ignore \
  PIP_DEFAULT_TIMEOUT=100 \
  PIP_CONSTRAINT='/usr/src/potree_backend/constraints.txt'

# Set project working directory
WORKDIR $APP_PATH

# Copy only requirements, to cache them in docker layer
COPY requirements.txt constraints.txt $APP_PATH/

# Installing necessary build tools and dependencies for Potree converter
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  cmake \
  git \
  libboost-all-dev \
  libeigen3-dev \
  libtbb-dev \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false

# Cleaning cache:
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --upgrade pip setuptools \
  && pip install -r requirements.txt

# Copy source code to project working directory
COPY . $APP_PATH