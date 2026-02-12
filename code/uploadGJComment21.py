from . import generateGJP2 as gjp2Gen
from . import readJSON
from . import generateCHK as chkGen
from . import getGJUsers20 as getAccID
import base64
import requests

def validate_account_id(account_id):
    """Validate the account ID."""
    if isinstance(account_id, int) and account_id > 0:
        return True
    return False

def validate_username(username):
    """Validate the username."""
    if isinstance(username, str) and 1 <= len(username) <= 30:
        return True
    return False

def validate_comment(comment):
    """Validate the comment."""
    if isinstance(comment, str) and 0 < len(comment) <= 100:
        return True
    return False

def validate_level_id(level_id):
    """Validate the level ID."""
    if isinstance(level_id, int) and level_id > 0:
        return True
    return False

def validate_percentage(percentage):
    """Validate the percentage completed."""
    return isinstance(percentage, int) and 0 <= percentage <= 100

def uploadGJComment21(userName: str, comment: str, levelID: int, percentage: int, password: str):

    accountID = getAccID.getGJUsers20(userName, type=1)
    if not validate_account_id(accountID):
        return "Invalid Account ID!"
    if not validate_username(userName):
        return "Invalid Username!"
    if not validate_comment(comment):
        return "Invalid Comment!"
    if not validate_level_id(levelID):
        return "Invalid Level ID!"
    if not validate_percentage(percentage):
        return "Percentage must be between 0 and 100!"
    gjp2 = gjp2Gen.generate_gjp2(password, "mI29fmAnxgTs")
    encoded_comment = base64.urlsafe_b64encode(comment.encode()).decode()
    chk = chkGen.generate_commentChk("29481", values = (userName + encoded_comment + str(levelID) + str(percentage)), salt = "0xPT6iUrtws0J")
    data = {
        "accountID": accountID,
        "gjp2": gjp2,
        "userName": userName,
        "comment": encoded_comment,
        "levelID": levelID,
        "percent": percentage,
        "chk": chk,
        "secret": "Wmfd2893gb7"
    }
    headers = {
        "User-Agent": "",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    request = requests.post("http://www.boomlings.com/database/uploadGJComment21.php", headers=headers, data=data)
    if request.status_code != -1:
        return "Comment posted successfully. Comment ID: " + request.text
    else:
        return "Request failed!"