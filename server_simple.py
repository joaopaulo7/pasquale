from flask import Flask, request
import os
import sys
from urllib.parse import urlparse, parse_qs
from difflib import SequenceMatcher
from time import sleep
import pasquale

app = Flask(__name__)
p = pasquale.Pasquale()


def generate_matches(corrections):
    matches = []
    for correction in corrections:
        match = {
            "message": "",
            "shortMessage": correction['reason'],
            "offset": correction['char_start'],
            "length": correction['len'],
            "replacements": [
                {
                    "value": correction['added']
                }
            ],
            "context": {
                "text": "this is is a palce holder context",
                "offset": 10,
                "length": 10
            },
            "sentence": "sentence",
            "rule": {
                "id": "string",
                "subId": "string",
                "description": "string",
                "urls": [
                    {
                        "value": "ruleurl"
                    }
                ],
                "issueType": "issueType",
                "category": {
                    "id": "string",
                    "name": "issueTypename"
                }
            }
        }
        matches.append(match)
    return matches



@app.route("/")
def main():
    return "hey, I'm working here!"


busy = False
last_resp = {}

from time import sleep
@app.route("/v2/check", methods=['POST'])
def check():
    global busy
    global last_resp
    if busy:
        return last_resp
    else:
        busy = True
    
    if request.content_type == 'text/json' or request.content_type == 'application/x-www-form-urlencoded':
        query = parse_qs(urlparse("dummy.com?"+request.get_data().decode('utf-8')).query)
        language = " ".join(query['language'])
        text = " ".join(query['text'])
    elif request.content_type == 'application/json':
        in_json = request.get_json()
        language = in_json['language']
        text     = in_json['text']
    else:
        raise TypeError("expected 'text/json', 'application/x-www-form-urlencoded' 'application/json' type, but got '"+request.content_type+"'")
    
    
    corrections = p.check(text, language, "formal, academic")
    
    busy = False
    last_resp = {
        "software": {
            "name": "pasquale",
            "version": "string",
            "buildDate": "string",
            "apiVersion": 0,
            "status": "string",
            "premium": True
        },
        "language": {
            "name": "string",
            "code": "string",
            "detectedLanguage": {
                "name": "string",
                "code": "string"
            }
        },
        "matches": generate_matches(corrections)
    }
    
    return last_resp

