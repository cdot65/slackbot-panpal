#!/bin/bash

OPENAI_TOKEN=${OPENAI_TOKEN}
SLACK_APP_TOKEN=${SLACK_APP_TOKEN}
SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN}

kubectl create secret generic slack-secrets --namespace=slackbots --from-literal=OPENAI_TOKEN=${OPENAI_TOKEN} --from-literal=SLACK_APP_TOKEN=${SLACK_APP_TOKEN} --from-literal=SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN}
