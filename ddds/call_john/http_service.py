# -*- coding: utf-8 -*-

import json

from flask import Flask, request
from jinja2 import Environment

app = Flask(__name__)
environment = Environment()


def jsonfilter(value):
    return json.dumps(value)


environment.filters["json"] = jsonfilter

with open('call_john/contacts.json', "r") as phone_numbers:
    PHONE_NUMBERS = json.load(phone_numbers)

PHONE_NUMBERS["contact_john"]["mobile"] = "0701234567"
PHONE_NUMBERS["contact_john"]["work"] = "0736582934"
PHONE_NUMBERS["contact_john"]["home"] = "031122363"
PHONE_NUMBERS["contact_mary"]["mobile"] = "0706574839"
PHONE_NUMBERS["contact_mary"]["work"] = "0784736475"
PHONE_NUMBERS["contact_mary"]["home"] = "031847528"

print(f"---------------- PHONE NUMBERS : {PHONE_NUMBERS}")

#with open('call_john/contacts.json', "w") as phone_numbers: # dump needed for time_ddd bc user sets time
#    json.dump(PHONE_NUMBERS, phone_numbers)

def error_response(message):
    response_template = environment.from_string("""
    {
      "status": "error",
      "message": {{message|json}},
      "data": {
        "version": "1.0"
      }
    }
    """)
    payload = response_template.render(message=message)
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response


def query_response(value, grammar_entry):
    response_template = environment.from_string("""
    {
      "status": "success",
      "data": {
        "version": "1.1",
        "result": [
          {
            "value": {{value|json}},
            "confidence": 1.0,
            "grammar_entry": {{grammar_entry|json}}
          }
        ]
      }
    }
    """)
    payload = response_template.render(value=value, grammar_entry=grammar_entry)
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response


def validator_response(is_valid):
    response_template = environment.from_string("""
    {
      "status": "success",
      "data": {
        "version": "1.0",
        "is_valid": {{is_valid|json}}
      }
    }
    """)
    payload = response_template.render(is_valid=is_valid)
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/dummy_query_response", methods=['POST'])
def dummy_query_response():
    response_template = environment.from_string("""
    {
      "status": "success",
      "data": {
        "version": "1.1",
        "result": [
          {
            "value": "dummy",
            "confidence": 1.0,
            "grammar_entry": null
          }
        ]
      }
    }
     """)
    payload = response_template.render()
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/action_success_response", methods=['POST'])
def action_success_response():
    response_template = environment.from_string("""
   {
     "status": "success",
     "data": {
       "version": "1.1"
     }
   }
   """)
    payload = response_template.render()
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/call", methods=['POST'])
def call():
  print(f"phone numbers: {PHONE_NUMBERS}")
  payload = request.get_json() # converts the JSON object into Python data
  print(f"payload: {payload}")
  selected_contact = payload["request"]["parameters"]["selected_contact"]["value"]
  print(f"phone numbers: {PHONE_NUMBERS}")
  selected_phone_type = payload["context"]["facts"]["selected_phone_type"]["value"]
  number = PHONE_NUMBERS.get(selected_contact, {}).get(selected_phone_type)
  print(f"payload: {payload}")
  print('got_json')
  return action_success_response()

@app.route("/phone_number", methods=['POST'])
def phone_number():
  print(f"phone numbers: {PHONE_NUMBERS}")
  payload = request.get_json() # converts the JSON object into Python data 

  selected_contact = payload["request"]["parameters"]["selected_contact"]["value"]
  selected_phone_type = payload["context"]["facts"]["selected_phone_type"]["value"]
  
  number = PHONE_NUMBERS.get(selected_contact, {}).get(selected_phone_type)
  return query_response(value=number, grammar_entry=None)