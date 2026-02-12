import requests
import base64
import readJSON as readJson
import generateGJP2 as genGjp2

def uploadGJAccComment20(accountID, password, comment):
    gjp2 = genGjp2.generate_gjp2(password, "mI29fmAnxgTs")
    encoded_comment = base64.urlsafe_b64encode(comment.encode()).decode()
    data = {
        "accountID": accountID,
        "gjp2": gjp2,
        "comment": encoded_comment,
        "secret": "Wmfd2893gb7"
    }
    headers = {
        "User-Agent": "",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    request = requests.post("http://www.boomlings.com/database/uploadGJAccComment20.php", headers=headers, data=data).text
    return request