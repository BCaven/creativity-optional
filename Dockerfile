# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

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
COPY . .

# TODO: in the final product, this will be built beforehand, 
# and the files will already be in src/
# so these lines will be obsolete
# remember to also adjust the dockerignore accordingly
# build vue site
#RUN --mount=type=cache,target=/root/.cache/vue-npm \
#    --mount=type=bind,source=vue-frontend/package.json,target=vue-frontend/package.json \
#    npm --prefix vue-frontend/ install
#RUN --mount=type=cache,target=/root/.cache/vue-install \
#    --mount=type=bind,source=vue-frontend/,target=vue-frontend/ \
#    npm --prefix vue-frontend/ run build

# Switch to the non-privileged user to run the application.
USER appuser



# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD flask --app src/flask_server run -p 8000 -h 0.0.0.0 --debug
    
