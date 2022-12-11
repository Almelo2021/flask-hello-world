from flask import Flask, request
import requests
import openai
import json
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World Cup!'

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'Robin' in incoming_msg:
        url = "https://api.openai.com/v1/completions"
        payload = json.dumps({
          "model": "text-curie-001",
          "prompt": "Question: What song did Maroon 5 and Future collab on? Respond with the first line of the lyrics.\n\nAnswer:",
          "temperature": 0.7,
          "max_tokens": 256,
          "top_p": 1,
          "frequency_penalty": 0,
          "presence_penalty": 0
        })
        headers = {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer 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'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        r = response.json()
        try:
            quote = r["choices"][0]["text"]
        except:
            quote = r["error"]["message"]
        msg.body(quote)
        responded = True
    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    return str(resp)
