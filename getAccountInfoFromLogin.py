import requests

def getAccountInfoFromLogin(username: str) -> tuple[int, int]:
    data = {
        "str": username,
        "secret": "Wmfd2893gb7"
    }
    headers = {
        "User-Agent": "",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    request = requests.post("http://www.boomlings.com/database/getGJUsers20.php", headers=headers, data=data).text
    
    if request != "-1":
        users = request.split("|")
        for user_string in users:
            parts = user_string.split(":")
            for i in range (0, len(parts), 2):
                if i + 1 >= len(parts):
                    break
                try:
                    key = int(parts[i])
                    value = parts[i + 1]
                except ValueError:
                    continue
                if key == 2:
                    userID = int(value)
                elif key == 16:
                    accountID = int(value)
        return userID, accountID
    else:
        return None, None