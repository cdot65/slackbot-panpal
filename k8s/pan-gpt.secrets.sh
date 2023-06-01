#!/bin/bash

# If arguments are passed, use those. Otherwise, use environment variables.
if [ $# -eq 3 ]; then
    OPENAI_TOKEN=$1
    SLACKBOT_PANGPT_APP_TOKEN=$2
    SLACKBOT_PANGPT_BOT_TOKEN=$3
else
    OPENAI_TOKEN=${OPENAI_TOKEN}
    SLACKBOT_PANGPT_APP_TOKEN=${SLACKBOT_PANGPT_APP_TOKEN}
    SLACKBOT_PANGPT_BOT_TOKEN=${SLACKBOT_PANGPT_BOT_TOKEN}
fi

# Check that all variables are set.
if [[ -z ${OPENAI_TOKEN} ]] || [[ -z ${SLACKBOT_PANGPT_APP_TOKEN} ]] || [[ -z ${SLACKBOT_PANGPT_BOT_TOKEN} ]]; then
    echo "All three environment variables OPENAI_TOKEN, SLACKBOT_PANGPT_APP_TOKEN, and SLACKBOT_PANGPT_BOT_TOKEN must be set."
    echo "You can add these to your .bashrc or .zshrc file as follows:"
    echo "export OPENAI_TOKEN=<your_openai_token>"
    echo "export SLACKBOT_PANGPT_APP_TOKEN=<your_SLACKBOT_PANGPT_APP_TOKEN>"
    echo "export SLACKBOT_PANGPT_BOT_TOKEN=<your_SLACKBOT_PANGPT_BOT_TOKEN>"
    echo "Then reload your shell with the command 'source ~/.bashrc' or 'source ~/.zshrc'"
    echo "Alternatively, pass these as arguments when running this script."
    exit 1
fi

kubectl create secret generic slack-secrets --namespace=slackbot --from-literal=OPENAI_TOKEN=${OPENAI_TOKEN} --from-literal=SLACKBOT_PANGPT_APP_TOKEN=${SLACKBOT_PANGPT_APP_TOKEN} --from-literal=SLACKBOT_PANGPT_BOT_TOKEN=${SLACKBOT_PANGPT_BOT_TOKEN}
