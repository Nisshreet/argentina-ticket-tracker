import requests

BOT_TOKEN = "8793009244:AAHU9I0umOKJsUOAjrVgWi8kHjMRtSA_T2g"
CHAT_ID = "7381610071"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=data)

    print(response.text)