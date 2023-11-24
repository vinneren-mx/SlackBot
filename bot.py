import slack
from flask import Flask
from slackeventsapi import SlackEventAdapter
from openAiFunctions import OpenAiFunctions
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
import os
openAi = OpenAiFunctions()
SLACK_TOKEN =  os.getenv('SLACK_TOKEN')
SIGNING_SECRET =  os.getenv('SIGNING_SECRET')

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)
 
client = slack.WebClient(token=SLACK_TOKEN)
 
@slack_event_adapter.on('message')
def message(payload):
    print(payload)
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    subtype = event.get('subtype')
    if subtype == "file_share":
        file = event.get('files')[0]
        print(file)
        
        client.chat_postMessage(channel=channel_id,text=f"Enviaste un archivo {file['filetype']}, en un momento lo proceso")
        openAi.uploadFile(file['url_private'])
        client.chat_postMessage(channel=channel_id,text=f"Se ha guardado correctamente tu archivo")
    if "compleation" in text:
        text = text.split("compleation:")
        response = openAi.compleation(text[1])
        text = f'{response.choices[0].message.content}'
        client.chat_postMessage(channel=channel_id, text=text)
    if text == "hi":
        client.chat_postMessage(channel=channel_id,text="Hello")

    
if __name__ == "__main__":
    app.run(debug=True)