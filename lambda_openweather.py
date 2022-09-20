import json
import requests
import datetime  
import pytz
import boto3

def lambda_handler(event, context):
    query = {'q':'gurgaon,in', 'units':'metric', 'APPID' : '4324efc8b49587301d3d1d043f171132'}
    response = requests.get("http://api.openweathermap.org/data/2.5/weather", params=query)
    weather=response.json()
    print(weather)
    main=weather["main"]
    sys=weather["sys"]
    sky=weather["weather"]
    
    epoch_time_sunrise = sys["sunrise"]
    epoch_time_sunset = sys["sunset"]
      
    # using the datetime.fromtimestamp() function  
    current_date_time = datetime.datetime.now(tz=pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d %I:%M %p")
    sunrise = datetime.datetime.fromtimestamp(epoch_time_sunrise).astimezone(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d %I:%M %p")
    sunset = datetime.datetime.fromtimestamp(epoch_time_sunset).astimezone(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d %I:%M %p")
   
    
    client = boto3.client('sns', region_name='us-east-1')
    topic_arn = "arn:aws:sns:us-east-1:848880885953:openweather-sns"
    
    sub="Weather update for Gurgaon, India"
    
    msg=f"Hi Deepak,\n"
    msg+=f"\n"
    msg+=f"Good Morning!\n"
    msg+=f"\n"
    msg+=f"Here is your weather update for {current_date_time}!\n"
    msg+=f"\n"
    msg+=f"Currently weather looks like {sky[0]['main']}\n"
    msg+=f"\n"
    msg+=f"Current temperatue is {main['temp']}℃ though feels like {main['feels_like']}℃. Today temperatue would be"
    msg+=f" in between min - {main['temp_min']}℃ and max - {main['temp_max']}℃ with wind pressure {main['pressure']} hPa and humidity"
    msg+=f" {main['humidity']}%\n"
    msg+=f"\n"
    msg+=f"Today's Sunrise - {sunrise} and Subset - {sunset}\n"
    msg+=f"\n"
    msg+=f"Have a wonderful day ahead\n"
    msg+=f"\n"
    msg+=f"Regards\n"
    msg+=f"Weather Team"
    
    try:
        client.publish(TopicArn=topic_arn, Message=msg, Subject=sub)
        result = 1
    except Exception:
        result = 0
    
    return result
