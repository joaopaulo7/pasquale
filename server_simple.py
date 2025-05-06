from flask import Flask, request
import os
import sys
from threading import Condition
from urllib.parse import urlparse, parse_qs
from difflib import SequenceMatcher
import pasquale

import time
import random

app = Flask(__name__)
s = SequenceMatcher()
p = pasquale.Pasquale()

cv = Condition()
queued = 0

current_text = ""
last_text = ""
last_resp = {}

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
    global counter
    with cv:
        print("IN\n")
        counter += 1
        cv.notify()
        cv.wait()
        print(counter)
    return "hey, I'm working here!"


@app.route("/v2/check", methods=['POST'])
def check():        
    if request.content_type == 'text/json' or request.content_type == 'application/x-www-form-urlencoded':
        query = parse_qs(urlparse("dummy.com?"+request.get_data().decode('utf-8')).query)
        language = " ".join(query['language'])
        text = " ".join(query['text'])
    elif request.content_type == 'application/json':
        in_json = request.get_json()
        language = in_json['language']
        text     = in_json['text']
    else:
        raise TypeError("expected 'text/json', 'application/x-www-form-urlencoded' or 'application/json' type, but got '"+request.content_type+"'")
    
    global last_text
    global current_text
    global last_resp
    global queued
        
    with cv:
        current_text = text
        cv.notify()
        
    with cv:
        notified = cv.wait(3.0)
        if notified:
            if text == current_text[:len(text)] and text[:len(last_text)] == last_text:
                return last_resp
        
        last_text = text
        corrections = p.check(text, language, "formal, acadêmico", "gemma3:1b-it-qat")
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

app.run(threaded=True)
