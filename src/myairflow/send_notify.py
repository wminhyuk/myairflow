import requests
import os

def send_noti(msg):

    WEBHOOK_ID = os.getenv("DISCORD_WEBHOOK_ID")
    WEBHOOK_TOKEN = os.getenv("DISCORD_WEBHOOK_TOKEN")
    WEBHOOK_URL = f"https://discordapp.com/api/webhooks/{WEBHOOK_ID}/{WEBHOOK_TOKEN}"
    data = {
        "content": msg
    }
    response = requests.post(WEBHOOK_URL, json=data)
    
    status_code = response.status_code
    if response.status_code == 204:
        print("Successfully sent message to Discord by wminhyuk", msg)
    else:
        print("Failed to send message to Discord by wminhyuk")
    return status_code
