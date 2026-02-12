import base64
import hashlib
from . import readJSON
from . import xor

def generate_commentChk(key = "29481", values = "", salt: str = "0xPT6iUrtws0J") -> str:
    values += salt
    string = ("").join(map(str, values))

    hashed = hashlib.sha1(string.encode()).hexdigest()
    xored = xor.cycled_xor(hashed, key)
    final = base64.urlsafe_b64encode(xored.encode()).decode()
    return final

def generate_leaderboardChk(key: int = 39673, values: list = [], salt: str = "yPg6pUrtWn0J") -> str:
    values.append(salt)
    string = ("").join(map(str, values))

    hashed = hashlib.sha1(string.encode()).hexdigest()
    xored = xor.cycled_xor(hashed, key)
    final = base64.urlsafe_b64encode(xored.decode().encode()).decode()

    return final