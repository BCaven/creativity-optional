# syntax=docker/dockerfile:1

# TODO: clean this up so it doesnt have a bunch of weird paths

# reference for new people
# https://docs.docker.com/go/dockerfile-reference/

ARG PYTHON_VERSION=3.11.4
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Get dependencies from apt
RUN --mount=type=cache,target=/root/.cache/apt \
    --mount=type=bind,source=docker-apt-requirements.txt,target=docker-apt-requirements.txt \
    apt-get update && \
    apt-get install -y $(cat docker-apt-requirements.txt)

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=docker-pip-requirements.txt,target=docker-pip-requirements.txt \
    python -m pip install -r docker-pip-requirements.txt


# Copy the source code into the container.
COPY src/ src/

# copy the front-end source over
# NOTE: this is the development server!
COPY vue-frontend/ vue-frontend/
# for release builds the frontend will be built in advance so the `vue-frontend/` folder will not actually be
# in the docker image

# TODO: make sure the files get sent to the right spot
# NOTE: in the final product, this will be built beforehand, 
# and the files will already be in src/
# build vue site
# change the working dir so npm does not get confused
WORKDIR /app/vue-frontend
RUN --mount=type=cache,target=/root/.cache/vue-npm \
    --mount=type=bind,source=vue-frontend/package.json,target=vue-frontend/package.json \
    npm install
RUN --mount=type=cache,target=/root/.cache/vue-install \
    --mount=type=bind,source=vue-frontend/,target=vue-frontend/ \
    npm run build

WORKDIR /app

# Switch to the non-privileged user to run the application.
USER appuser



# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
# TODO: change this to a production server (when the time comes)
CMD python3 src/flask_server.py
    
