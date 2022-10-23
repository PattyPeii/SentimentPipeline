import requests
import os
import json

def get_sentiment(config, text):
    url = config["NLP_API"]["url"]
    key = config["NLP_API"]["key"]

    querystring = {"text":f"{text}"}

    headers = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "twinword-sentiment-analysis.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.text

def construct_msg(json_msg, sentiment):
    msg = {"sentiment":sentiment}
    json_msg.update(msg)
    return json_msg

