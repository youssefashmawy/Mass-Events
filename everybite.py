import requests
TOKEN = "DWIR5FUPSH2RISX56NGG"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

# Search for upcoming events in Bucharest
url = "https://www.eventbriteapi.com/v3/events/search/"
params = {
    "location.address": "Egypt",
    "sort_by": "date",
    "start_date.range_start": "2025-09-01T00:00:00Z",  
    "start_date.range_end": "2025-12-31T23:59:59Z"     
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

for event in data.get("events", []):
    print(f"Event: {event['name']['text']} | Start: {event['start']['local']} | URL: {event['url']}")