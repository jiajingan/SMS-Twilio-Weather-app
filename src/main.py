from twilio.rest import Client
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import requests, json
load_dotenv()

app = Flask(__name__)

# # Your Account SID from twilio.com/console
account_sid = os.getenv('sid')
# # Your Auth Token from twilio.com/console
auth_token  = os.getenv('twilio_token')

# # Your twilio number

client = Client(account_sid, auth_token)

# message = client.messages.create(
#     to=os.getenv('to_number'), 
#     from_=os.getenv('from_number'),
#     body="Hello from Python!")

# print(message.sid)
weather_api_key = os.getenv('weather_key')
base_url = "http://api.openweathermap.org/data/2.5/weather?"
# def automatedText(message,time,weatherSMS):
#     if('-a' in message):
#         message = client.messages.create(
#             to=os.getenv('to_number'), 
#             from_=os.getenv('from_number'),
#             body=weatherSMS)
    
    

def replyMessage(message):
    message = message.lower().strip()
    city_name = message.replace("weather ", "")
    complete_url = base_url + "appid=" + weather_api_key + "&q=" + city_name + "&units=imperial"
    response = requests.get(complete_url)
    x = response.json()

    if "weather help" == message:
        message = "type [weather 'city'] to get weather data"
    elif ("weather" not in message) or ("weather" == message):
        message = "Sorry we have a problem processing your text, please try again.\nType [weather help] for help"
    elif "weather" in message:
        if x["cod"] != "404":
            temp = x['main']['temp']
            humidity = x['main']["humidity"]
            weather_description = x["weather"][0]["description"]
            message = f"""Temperature: {temp}°F\nHumidity: {humidity}\nDescription: {weather_description}"""
        else:
            message = "Sorry the City is Not Found"
    return message


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a MMS message."""
    # Start our TwiML response
    message_body = request.form['Body']
    resp = MessagingResponse()
    replyText = replyMessage(message_body)
    resp.message(replyText)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
