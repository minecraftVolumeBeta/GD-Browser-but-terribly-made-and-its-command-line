from . import getGJUserInfo20 as getHisProfile
import requests

def getGJUsers20(searchStr: str = "", type: int = 0):
    data = {
        "str": searchStr,
        "secret": "Wmfd2893gb7"
    }
    headers = {
        "User-Agent": "",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        request = requests.post("http://www.boomlings.com/database/getGJUsers20.php", headers=headers, data=data).text
    except Exception as e:
        print(f"Request failed: {e}")
        return

    if request == "-1":
        print("No users found.")
        return

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
            if key == 16:
                accountID = int(value)
                if type == 0:
                    print(f"\nFetching profile for AccountID: {accountID}\n")
                    getHisProfile.getGJUserInfo20(accountID)
                    break
                elif type == 1:
                    return accountID