"""
FastAPI server to redirect firewall log messages to ChatGPT for troubleshooting.
"""

import os
from typing import Dict

from fastapi import FastAPI, status, HTTPException, Body
from fastapi.openapi.utils import get_openapi
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi import SlackRequestHandler
import openai


app = FastAPI()

openai.api_key = os.environ.get("OPENAI_TOKEN")
openai_engine = "gpt-4"
slack_app = AsyncApp(token=os.environ.get("SLACKBOT_PANGPT_APP_TOKEN"))
handler = SlackRequestHandler(slack_app)


@app.on_event("startup")
async def startup_event():
    """
    Event handler that runs when the app starts up.
    """
    app.openapi_schema = None


@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_schema():
    """
    Endpoint that returns the OpenAPI schema for the app.
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="ChatGPT API",
        version="0.1.0",
        description="API for interacting with OpenAI's GPT-3 chatbot",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


@app.post("/pangpt/decryption/")
async def decryption_message_receiver(body: Dict[str, str] = Body(...)):
    """
    Endpoint that receives a JSON-formatted log message from a Palo Alto Networks firewall and sends it to ChatGPT
    for troubleshooting. The response from ChatGPT is sent to a Slack channel as a structured Slack message.

    Args:
        body (Dict[str, str]): The JSON-formatted log message from the firewall.

    Raises:
        HTTPException: Raised if there is an error while processing the request.

    Returns:
        int: The HTTP status code for the response (200 for success).
    """
    request = """
    You are an AI bot specialized in the network and cybersecurity industry, particularly trained with expertise in Palo Alto Networks PAN-OS firewalls. I will feed you a JSON formatted log message from a firewall and your task will be to troubleshoot the decryption log, paying close attention to the value of "error". Your response should employ the given Jinja2 template, and also include a succinct sentence suggesting the next steps based on the "error" value. Avoid providing any explanations; simply return the output of the Jinja2 template along with your recommendation.

    Here is the Jinja2 template for your reference:

    - name: {{ device_name }}
      sni: {{ sni }}
      commonname: {{ cn }}
      root: {{ root_cn }}
      rootstatus: {{ root_status }}
      details: {{ error }}
      sourceip: {{ src }}
      sourceuser: {{ srcuser }}
      destinationip: {{ dst }}
      application: {{ app }}

    Apply this template to the JSON log message and provide your analysis and recommendation.
    """
    try:
        response = openai.ChatCompletion.create(
            model=openai_engine,
            messages=[
                {"role": "system", "content": f"{request}."},
                {"role": "user", "content": f"{body}"},
            ],
        )
        message = response.choices[0]["message"]
        msg = message.to_dict_recursive()
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "```\n" + str(msg["content"]) + "\n```",
                },
            }
        ]
        await slack_app.client.chat_postMessage(
            channel=os.environ.get("SLACK_CHANNEL", ""),
            blocks=blocks,
            text="Here's the message content:",
            token=os.environ.get("SLACKBOT_PANGPT_BOT_TOKEN", ""),
        )
        return status.HTTP_200_OK
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@app.post("/pangpt/globalprotect/")
async def globalprotect_message_receiver(body: Dict[str, str] = Body(...)):
    """
    Endpoint that receives a JSON-formatted log message from a Palo Alto Networks firewall and sends it to ChatGPT
    for troubleshooting. The response from ChatGPT is sent to a Slack channel as a structured Slack message.

    Args:
        body (Dict[str, str]): The JSON-formatted log message from the firewall.

    Raises:
        HTTPException: Raised if there is an error while processing the request.

    Returns:
        int: The HTTP status code for the response (200 for success).
    """
    request = """
    I want you to role play as a bot that specializes within the network and cybersecurity industry, specifically with Palo Alto Networks PAN-OS firewalls.
    You will be fed a JSON formatted log message from the firewall and will be tasked with troubleshooting the Global Protect log below.
    Your response will be detailed troubleshooting information. Include affected users, affected devices, and any other information that would be helpful to the user.
    Your response will not reference yourself, will be without pronouns, and will be written in the third person as a Slack message.
    The response needs to be structured in Slack Block format as it will be sent to the user as a Slack message.
    """
    try:
        response = openai.ChatCompletion.create(
            model=openai_engine,
            messages=[
                {"role": "system", "content": f"{request}."},
                {"role": "user", "content": f"{body}"},
            ],
        )
        message = response.choices[0]["message"]
        msg = message.to_dict_recursive()
        blocks = [
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": msg["content"]},
            }
        ]
        await slack_app.client.chat_postMessage(
            channel=os.environ.get("SLACK_CHANNEL", ""),
            blocks=blocks,
            token=os.environ.get("SLACKBOT_PANGPT_BOT_TOKEN", ""),
        )
        return status.HTTP_200_OK
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
