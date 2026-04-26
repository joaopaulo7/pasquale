import os
import yaml

from flask import Flask, request, render_template
from threading import Condition
from urllib.parse import urlparse, parse_qs

import pasquale as pasq
import page_builder as pb


CONFIG_FILE = os.getenv("CONFIG_FILE")
HOST = os.getenv("PASQUALE_HOST", "127.0.0.1")
PORT = int(os.getenv("PASQUALE_PORT", 5000))

app = Flask(__name__)
cond = Condition()

if CONFIG_FILE:
    pasquale = pasq.Pasquale(config_file=CONFIG_FILE)
else:
    pasquale = pasq.Pasquale()

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
    return render_template("config.html",
                           page_name = "I'm workin' here!",
                           form = "")


@app.route("/config")
def config():
    form =  pb.get_form(
        creds = pasquale.creds,
        config = pasquale.config,
        options = {"prompt_type": pasquale.prompts})
    return render_template("config.html",
                           page_name = "Parameter Configuration",
                           form = form)


def try_convert_to_float(value: str | int):
    try:
        return float(value)
    except:
        return value


@app.route("/config", methods=["POST"])
def set_config():
    creds = {}
    config = {}

    for key, value in request.form.items():
        if value.isnumeric():
            value = int(value)
        else:
            value = try_convert_to_float(value)
        
        if key in {"api_key", "base_url"}:
            creds[key] = value
        else:
            config[key] = value
    
    full_config = {"creds":creds, "config": config}

    pasquale.set_config(full_config)
    with open("config.yaml", "w") as out_file:
        yaml.dump(full_config,
                  out_file)

    return render_template("config.html",
                           page_name = "Parameter Configuration",
                           form = "Parameters reconfigured!  =)")
    

@app.route("/v2/check", methods=["POST"])
async def check():        
    if request.content_type == "text/json" or request.content_type == "application/x-www-form-urlencoded":
        query = parse_qs(urlparse("dummy.com?"+request.get_data().decode('utf-8')).query)
        language = " ".join(query["language"])
        text = " ".join(query["text"])
    elif request.content_type == "application/json":
        in_json = request.get_json()
        language = in_json["language"]
        text     = in_json["text"]
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
    app.run(threaded=True, host=HOST, port=PORT)
