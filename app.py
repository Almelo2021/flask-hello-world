from flask import Flask, request
import requests
import config
import openai
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
        openai.api_key = config.api_key
        # return a quote
        r = openai.Completion.create(
            model="text-curie-001",
            prompt="Question: "+incoming_msg+"\n\nAnswer:",
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
        if r["choices"][0]["finish_reason"] == "stop":
            quote = r["choices"][0]["text"]
        else:
            quote = "I don't know at this time, sorry."
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
    if not responded:
        msg.body('I only know about famous quotes and cats, sorry!')
    return str(resp)
