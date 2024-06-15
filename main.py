import requests
import json
from datetime import datetime
import os

GENDER = "XXXXX" # Modify as necessary
WEIGHT_KG = 111 # Modify as necessary
HEIGHT_CM = 111 # Modify as necessary
AGE = 111 # Modify as necessary

# Get environment variables
APP_ID = os.environ.get("APP_ID")
APP_KEY = os.environ.get("APP_KEY")
SHEETY_USER = os.environ.get("SHEETY_USER")
SHEETY_BEARER_TOKEN = os.environ.get("SHEETY_BEARER_TOKEN")

# API endpoints
api_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
api_endpoint_sheety = f"https://api.sheety.co/{SHEETY_USER}/workouts/workouts"

# Request exercise information
exercise_text = input("What exercises did you do today?")
headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
}
exercise_parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

# Make the request to Nutritionix
response = requests.post(url=api_endpoint, json=exercise_parameters, headers=headers)
data = response.json()
print(data)
num_calories = data["exercises"][0]["nf_calories"]
duration_min = data["exercises"][0]["duration_min"]
name = data["exercises"][0]["name"]

# Get the current date and time
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

# Create a new row for Sheety
new_row = {
    "workout": {
        "date": today_date,
        "time": now_time,
        "exercise": name.title(),
        "duration": duration_min,
        "calories": num_calories
    }
}
headers = {
    "Authorization": f"Bearer {SHEETY_BEARER_TOKEN}"
}

# Make the POST request to Sheety
response = requests.post(url=api_endpoint_sheety, json=new_row, headers=headers)
