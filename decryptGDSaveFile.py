import base64
import gzip
import readJSON
import xor

def decryptGDSaveFile(filePath: str = ""):
    try:
        with open(filePath, 'r') as file:
            content = file.read()
            decrypted_data = decrypt_data(content)
            return decrypted_data
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
def decrypt_data(data: str) -> str:
    if not data:
        return ""
    gunzipped = gzip.decompress(data.encode('utf-8'))
    base64_decoded = base64.urlsafe_b64decode(gunzipped).decode('utf-8')
    xored = xor.singular_xor(base64_decoded, key=11)
    return xored