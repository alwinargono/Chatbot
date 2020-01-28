from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from utils import fetch_reply
import json, requests
import time

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

def getweather(city):
    api_key = "7298d140cd7a01576caac3c583586bb1"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = city
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
    response = requests.get(complete_url) 
    x = response.json() 
    if x["cod"] != "404": 
        y = x["main"] 
        current_temperature = y["temp"] 
        temp = current_temperature - 273.15
        disp_temp = int(temp)
        return str(disp_temp)
    else:
        disp_temp = "city not found"
  

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body').lower()
    resp = MessagingResponse()

    if "hi" in msg or "hello" in msg:
        resp.message("Greetings Human! I am a weather bot!                                                                             To get the weather of a current city type in \"weather celcius/farenheit in cityname\"")

    if "weather" in msg and "celcius" in msg:
        string1 = msg
        cty = string1.split("in ",1)[1]
        resp.message("it's "+ getweather(cty) + " Celcius in " +cty)
    
    elif "weather" in msg and "farenheit" in msg:
        string1 = msg
        cty = string1.split("in ",1)[1]
        number = getweather(cty)
        infarenheit = (number * 9/5) + 32
        resp.message("it's "+ infarenheit + " Farenheit in " +cty)
    else:
        resp.message("Please Try again!")




    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)