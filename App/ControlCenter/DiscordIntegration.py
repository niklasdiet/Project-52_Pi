import requests, json

def sendDiscordMessage(message, url):
    data = {}
    data["content"] = message
    result = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    
    if result.status_code == 204:
        return True
    else:
        return False