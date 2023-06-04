FROM python:3-alpine

# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------
LABEL name="ghcr.io/cdot65/slackbot-panpal"
LABEL maintainer="cremsburg.dev@gmail.com"
LABEL description="FastAPI server to redirect logs to ChatGPT for troubleshooting."
LABEL license="Apache 2.0"
LABEL url="https://github.com/cdot65/slackbot-pan-gpt"
LABEL build-date="20230601"

# ---------------------------------------------------------------------------
# Install dependencies and Python packages
# ---------------------------------------------------------------------------
ADD requirements.txt /var/tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /var/tmp/requirements.txt

# ---------------------------------------------------------------------------
# Copy source code
# ---------------------------------------------------------------------------
COPY ./app /code/app
WORKDIR /code

# ---------------------------------------------------------------------------
# Run the application
# ---------------------------------------------------------------------------
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
