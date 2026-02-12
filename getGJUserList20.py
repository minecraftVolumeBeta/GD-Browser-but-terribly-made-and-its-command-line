import requests
import generateGJP2
import getGJUserInfo20

def getGJUserList20(accountID: int = 0, password: str = "", type: int = 0):
    gjp2 = generateGJP2.generate_gjp2(password, "mI29fmAnxgTs")
    data = {
        "accountID": accountID,
        "gjp2": gjp2,
        "type": type,
        "secret": "Wmfd2893gb7"
    }
    headers = {
        "User-Agent": "",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    request = requests.post("http://www.boomlings.com/database/getGJUserList20.php", headers=headers, data=data).text

    users = []
    if request == "-1" or not request:
        print("Error occurred or no users found.")
        return users
    user_entries = request.split("|")
    for entry in user_entries:
        users.append(getGJUserInfo20.parseuserInfo(entry))

    for user in users:
        print(user)