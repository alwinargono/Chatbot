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
        z = x["weather"]
        weather_desc = z[0]["description"]
        return str(disp_temp)
    else:
        disp_temp = "city not found"

def getdesc(city):
    api_key = "7298d140cd7a01576caac3c583586bb1"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = city
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
    response = requests.get(complete_url) 
    x = response.json() 
    if x["cod"] != "404": 
        y = x["main"] 
        z = x["weather"]
        weather_desc = z[0]["description"]
        return str(weather_desc)
    else:
        disp_temp = "city not found"
        return str(disp_temp)


@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body').lower()
    resp = MessagingResponse()

    if "hi" in msg or "hello" in msg:
        resp.message("Greetings Human! I am a weather bot!")                                                                             
        resp.message("To get the weather of the desired city type in \"weather in cityname\"")
        resp.message("To get the weather in farenheit type in \"farenheit in cityname\"")

    if "weather" in msg:
        string1 = msg
        cty = string1.split("in ",1)[1]
        resp.message("it's {} Celcius and {} in {}".format(getweather(cty),getdesc(cty),cty))
    
    if "farenheit" in msg:
        string1 = msg
        cty = string1.split("in ",1)[1]
        number = getweather(cty)
        number = int(number)
        infarenheit = (number * 9/5) + 32
        resp.message("it's "+ str(infarenheit) + " Farenheit and "+ getdesc(cty) + " in " + cty)
    
    if "bye" in msg:
        resp.message("Thank you for using the weather chatbot!")
        resp.message("Have a nice day!")




    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)