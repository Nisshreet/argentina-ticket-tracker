import requests

ACCESS_TOKEN = "o.s2Jiw9FgGoKlLrDew2rYCc3iHD8aID5z"

def send_notification(title, body):
    requests.post(
        "https://api.pushbullet.com/v2/pushes",
        headers={
            "Access-Token": ACCESS_TOKEN,
            "Content-Type": "application/json"
        },
        json={
            "type": "note",
            "title": title,
            "body": body
        }
    )