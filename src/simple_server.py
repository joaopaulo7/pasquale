import os

from flask import Flask, request
from threading import Condition
from urllib.parse import urlparse, parse_qs
import pasquale as pasq

CONFIG_FILE = os.getenv("CONFIG_FILE")

app = Flask(__name__)
cond = Condition()

pasquale = pasq.Pasquale(config_file=CONFIG_FILE)

current_text = ""
last_text = ""
last_resp = {}

def get_match(reason, char_start, length, corr_added):
    return {
        "message": "",
        "shortMessage": reason,
        "offset": char_start,
        "length": length,
        "replacements": [
            {
                "value": corr_added
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


def get_resp(matches):
    return {
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
        "matches": matches
    }


def generate_matches(corrections):
    matches = []
    for correction in corrections:
        match = get_match(
            reason = correction["reason"],
            char_start = correction["char_start"],
            length = correction["len"],
            corr_added = correction["added"],
        )
        matches.append(match)
    return matches


@app.route("/")
def main():
    return "hey, I'm working here!"


@app.route("/v2/check", methods=['POST'])
async def check():        
    if request.content_type == "text/json" or request.content_type == "application/x-www-form-urlencoded":
        query = parse_qs(urlparse("dummy.com?"+request.get_data().decode('utf-8')).query)
        language = " ".join(query['language'])
        text = " ".join(query['text'])
    elif request.content_type == "application/json":
        in_json = request.get_json()
        language = in_json['language']
        text     = in_json['text']
    else:
        raise TypeError("expected 'text/json', 'application/x-www-form-urlencoded' or 'application/json' type, but got '"+request.content_type+"' instead")
    
    global last_text
    global current_text
    global last_resp
    global queued
    
    # cond makes sure a sigle thread enters at a time
    with cond:
        current_text = text
        cond.notify()
    with cond:
        notified = cond.wait(3.0)

        # if current text mostly matches the last one in a 3s timespan,
        # don't update
        if (notified
            and text == current_text[:len(text)]
            and text[:len(last_text)] == last_text):
                return last_resp
        
        last_text = text
        corrections = await pasquale.check(text, language)
        last_resp = get_resp(generate_matches(corrections))
    
    return last_resp


if __name__ == "__main__":
    app.run(threaded=True, host="0.0.0.0", port=5000)
