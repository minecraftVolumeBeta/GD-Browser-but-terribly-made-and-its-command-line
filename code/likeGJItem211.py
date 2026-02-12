import requests
def likeGJItem211(itemID: int = 0, type: int = 1):
    data = {
        "itemID": itemID,
        "type": type,
        "secret": "Wmfd2893gb7"
    }
    headers = {
        "User-Agent": "",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.post("http://www.boomlings.com/database/likeGJItem211.php", headers=headers, data=data).text