import base64
import requests

def decodeAccComment(response: str):
    attributes = {
        2: "comment",
        3: "authorPlayerID",
        4: "likes",
        5: "dislikes",
        6: "commentID",
        8: "authorAccountID",
        9: "age"
    }
    comments_list = []

    parts = response.split(':')

    for i in range(0, len(parts), 2):
        if i + 1 < len(parts):
            key = int(parts[i])
            value = parts[i + 1]
            if key in attributes:
                comments_list.append((attributes[key], value))
            else:
                continue

        print(", ".join(f"{k}: {v}" for k, v in comments_list))
        print('-' * 40)

def getGJAccountComments20(accountID: int, page: int):
    data = {
        "accountID": accountID,
        "page": page,
        "secret": "Wmfd2893gb7"
    }
    headers = {
        "User-Agent": "",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    request = requests.post("http://www.boomlings.com/database/getGJAccountComments20.php", data=data, headers=headers).text

    if request == "-1":
        return ("Account not found or error occurred.", None)
    else:
        if ':' not in request:
            return ("No comments found.", None)
        else:
            decodeAccComment(request)