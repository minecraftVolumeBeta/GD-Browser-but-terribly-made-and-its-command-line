import base64
import hashlib
from . import readJSON
from . import xor

def generate_gjp2(password: str = "", salt: str = "mI29fmAnxgTs") -> str:
	password += salt
	hashed = hashlib.sha1(password.encode()).hexdigest()
	
	return hashed

def encode_gjp(password: str) -> str:
    encoded = xor.cycled_xor(password, "37526")
    encoded_base64 = base64.urlsafe_b64encode(encoded.encode()).decode()
    return encoded_base64