import requests
import os

# main reason why this is here:
# 1. catbox for some reason need this
# 2. this is probably required
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Origin": "https://catbox.moe",
    "Referer": "https://catbox.moe/",
}

def catbox(filePath):
    url = "https://catbox.moe/user/api.php"
    try:
        with open(filePath, "rb") as f:
            files = {"fileToUpload": (os.path.basename(filePath), f)}
            data = {"reqtype": "fileupload"}
            response = requests.post(url, data=data, files=files, headers=headers)

            if response.status_code == 200:
                result = response.text.strip()
                if result:
                    return result
                return "Error: Server returned empty response."
            return f"Server Error: {response.status_code}"
    except Exception as e:
        return f"Request Failed: {str(e)}"


def litterbox(filePath, duration="1h"):
    url = "https://litterbox.catbox.moe/resources/internals/api.php"
    try:
        with open(filePath, "rb") as f:
            files = {"fileToUpload": (os.path.basename(filePath), f)}
            data = {"reqtype": "fileupload", "time": duration}
            response = requests.post(url, data=data, files=files, headers=headers)

            if response.status_code == 200:
                result = response.text.strip()
                if result:
                    return result
                return "Error: Server returned empty response."
            return f"Server Error: {response.status_code}"
    except Exception as e:
        return f"Request Failed: {str(e)}"


def buzzheavier(filePath):
    filename = os.path.basename(filePath)
    url = f"https://w.buzzheavier.com/{filename}"
    try:
        with open(filePath, "rb") as f:
            response = requests.put(url, data=f, headers=headers)
            if response.status_code in [200, 201]:
                data = response.json()
                fileId = data.get("data", {}).get("id")
                if fileId:
                    return f"https://buzzheavier.com/{fileId}"
                return "Error: Could not find file ID in response."
            return f"Server Error: {response.status_code}"
    except Exception as e:
        return f"Request Failed: {str(e)}"
