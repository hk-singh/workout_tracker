import requests
import os
from datetime import datetime

APP_ID=os.environ.get("APP_ID")
NUTRITIONIX_API_KEY = os.environ.get("NUTRITIONIX_API_KEY")
DOMAIN = os.environ.get("DOMAIN")
FOOD_ENDPOINT = os.environ.get("FOOD_ENDPOINT")
EXERCISE_ENDPOINT = os.environ.get("EXERCISE_ENDPOINT")
SHEET_URL = os.environ.get("SHEET_URL")

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    "x-app-id": APP_ID,
    "x-app-key": NUTRITIONIX_API_KEY,
}

sheet_headers = {
    "Authorization": "Basic aGFyc2hrczpCbGFibGEuMTIzNDU2"
}

# food_query = input("Write down your food intake:")
# food_params = {
#     "query": food_query,
# }
#
exercise_query = input("What exercises did you do today?")
exercise_params = {
    "query": exercise_query,
}
#
# food_response = requests.post(url=f"{DOMAIN}{FOOD_ENDPOINT}", headers=headers, json=food_params)
# food_response.raise_for_status()
exercise_response = requests.post(url=f"{DOMAIN}{EXERCISE_ENDPOINT}", headers=headers, json=exercise_params)
exercise_data = exercise_response.json()
exercise_response.raise_for_status()

now = datetime.now()

workout_data = {
    "workout": {
        "date": now.strftime('%d/%m/%Y'),
        "time": now.strftime('%H:%M:%S'),
        "exercise": exercise_data["exercises"][0]["name"].title(),
        "duration": exercise_data["exercises"][0]["duration_min"],
        "calories": exercise_data["exercises"][0]["nf_calories"],
    }
}
#print(workout_data)
sheet_response = requests.post(url=SHEET_URL, headers=sheet_headers, json=workout_data)
sheet_response.raise_for_status()
#print(sheet_response.json())
