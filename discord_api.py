import requests
from config_manager import load_config



config = load_config()
TOKEN = config.get("TOKEN", "YOUR_TOKEN")
showUserIds = False

def send_message(channel, message):
    url = f"https://discord.com/api/v9/channels/{channel}/messages"
    headers = {"Authorization": TOKEN}
    data = {"content": message}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Message sent successfully to channel {channel}.")
    else:
        print(f"Failed to send the message. Status code: {response.status_code}")
        print(response.text)

def changeUserIdStatus():
    global showUserIds
    if showUserIds == True:
        showUserIds = False
    else:
        showUserIds = True
    print(showUserIds)


def get_latest_messages(channel, limit=10):
    url = f"https://discord.com/api/v9/channels/{channel}/messages?limit={limit}"
    headers = {"Authorization": TOKEN}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        messages = response.json()
        formatted_messages = []
        for message in messages:
            username = message["author"]["username"]
            userid = "<@"+ message["author"]["id"] + ">"
            content = message["content"]
            truncated_content = " ".join(content.split()[:35])
            if showUserIds == True:
                formatted_messages.append(f"[{username}] [{userid}] {truncated_content}")
            else:
                formatted_messages.append(f"[{username}] {truncated_content}")

        return formatted_messages
    return []
