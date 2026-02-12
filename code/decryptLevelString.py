import base64
import gzip
from . import xor

def decryptLevelString(levelString: str = ""):
    if not levelString:
        return ""
    base64_decoded = base64.urlsafe_b64decode(xor.singular_xor(levelString, key=11).encode())
    decompressed = gzip.decompress(base64_decoded)
    return decompressed.decode()