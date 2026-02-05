import requests
import os
import json

# Load secrets from GitHub Environment Variables
client_id = os.environ['STRAVA_CLIENT_ID']
client_secret = os.environ['STRAVA_CLIENT_SECRET']
refresh_token = os.environ['STRAVA_REFRESH_TOKEN']

# 1. Get a new Access Token
auth_url = "https://www.strava.com/oauth/token"
payload = {
    'client_id': client_id,
    'client_secret': client_secret,
    'refresh_token': refresh_token,
    'grant_type': 'refresh_token',
    'f': 'json'
}

print("Refreshing Access Token...")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']

# 2. Fetch Athlete Stats
# Replace 'YOUR_ATHLETE_ID' isn't needed; the token belongs to you, 
# so we can just ask for the authenticated athlete's stats.
# However, the stats endpoint requires the athlete ID.
# Let's get the athlete ID first to be safe, or you can hardcode it if you know it.
athlete_url = "https://www.strava.com/api/v3/athlete"
headers = {'Authorization': f'Bearer {access_token}'}
athlete = requests.get(athlete_url, headers=headers).json()
athlete_id = athlete['id']

print(f"Fetching stats for Athlete ID: {athlete_id}...")
stats_url = f"https://www.strava.com/api/v3/athletes/{athlete_id}/stats"
stats = requests.get(stats_url, headers=headers).json()

# 3. Save specific data to JSON
# We only need the "ytd_run_totals", "ytd_ride_totals", and "ytd_swim_totals"
output_data = {
    "run": {
        "count": stats['ytd_run_totals']['count'],
        "distance": int(stats['ytd_run_totals']['distance']), # in meters
        "moving_time": stats['ytd_run_totals']['moving_time'], # in seconds
        "elevation_gain": int(stats['ytd_run_totals']['elevation_gain']) # in meters
    },
    "ride": {
        "count": stats['ytd_ride_totals']['count'],
        "distance": int(stats['ytd_ride_totals']['distance']),
        "moving_time": stats['ytd_ride_totals']['moving_time'],
        "elevation_gain": int(stats['ytd_ride_totals']['elevation_gain'])
    },
    "swim": {
        "count": stats['ytd_swim_totals']['count'],
        "distance": int(stats['ytd_swim_totals']['distance']),
        "moving_time": stats['ytd_swim_totals']['moving_time'],
        "elevation_gain": 0 # Swims usually don't track elevation
    }
}

# Write to file
with open('strava_stats.json', 'w') as f:
    json.dump(output_data, f)

print("strava_stats.json updated successfully!")