import json
from flask import Flask
from flask_cors import CORS
import requests
import re
import ast
import openai
from decouple import config
openai.api_key = config("OPENAI_API_KEY")

def gpt3(input):

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[{"role": "user", "content": input}],
    temperature=0.7,
    max_tokens=512,
    )
    return completion.choices[0].message.content

def dict_to_json(d):
    return d.__dict__

app = Flask(__name__)
CORS(app)

db = json.load(open('db.json','r'))
print("INITIAL DB STATE")
print(db['todo_list']["state"])

@app.route('/<app_name>/<api_call>')
def api(app_name, api_call):
    db = json.load(open('db.json','r'))
    print("INPUT DB STATE")
    print(db[app_name]["state"])
    gpt3_input = f"""{db[app_name]["prompt"]}
API Call (indexes are zero-indexed):
{api_call}

Database State:
{db[app_name]["state"]}

Output the new database state as JSON.
"""
    response= gpt3(gpt3_input)
    print(response)
    db[app_name]["state"] = response
    json.dump(db, open('db.json', 'w'), indent=4)
    return response

if __name__ == "__main__":
    app.run()