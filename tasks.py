"""Tasks to execute with Invoke."""

# ---------------------------------------------------------------------------
# Python3.11 hack for invoke
# ---------------------------------------------------------------------------
import inspect

if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec

import os
from invoke import task

# ---------------------------------------------------------------------------
# DOCKER PARAMETERS
# ---------------------------------------------------------------------------
DOCKER_IMG = "ghcr.io/cdot65/pangpt"

DOCKER_TAG = "0.1.0"


# ---------------------------------------------------------------------------
# SYSTEM PARAMETERS
# ---------------------------------------------------------------------------
PWD = os.getcwd()


# ---------------------------------------------------------------------------
# DOCKER CONTAINER BUILDS
# ---------------------------------------------------------------------------
@task()
def build(context):
    """Build our Docker images."""
    context.run(
        f"docker build -t {DOCKER_IMG}:{DOCKER_TAG} .",
    )


# ---------------------------------------------------------------------------
# SHELL ACCESS
# ---------------------------------------------------------------------------
@task()
def shell(context):
    """Get shell access to the container."""
    context.run(
        f'docker run -it --rm \
            -w /code/app/ \
            {DOCKER_IMG}:{DOCKER_TAG} /bin/sh',
        pty=True,
    )

# ---------------------------------------------------------------------------
# FastAPI
# ---------------------------------------------------------------------------
@task()
def local(context):
    """Get access to the ipython REPL within our container."""
    context.run(
        f'docker run -it --rm \
            -p 8080:80 \
            -w /code \
            {DOCKER_IMG}:{DOCKER_TAG}',
        pty=True,
    )
