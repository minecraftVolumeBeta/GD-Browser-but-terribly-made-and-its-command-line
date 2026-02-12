from code import GDLevelData as levelData
from code import GDLevelSearch as levelSearch
from code import uploadGJAccComment20 as uploadComment
from code import uploadGJComment21 as uploadLevelComment
from code import decryptGDSaveFile as decryptSave
from code import likeGJItem211 as likeItem
from code import getGJComments21 as getComments
from code import getGJUsers20 as getProfile
from code import getAccountInfoFromLogin as getLoginInfo
from code import getGJUserList20 as getUserList
import sys
import json
import time
import getpass
import os
import base64
import zlib

# --- ENCRYPTION HELPERS ---

XOR_KEY = "2.01K0320"

def cycled_xor_bytes(data: bytes, key: str) -> bytes:
    """Performs a cyclic XOR on bytes data using a string key."""
    key_bytes = key.encode('utf-8')
    result = bytearray(len(data))
    for i in range(len(data)):
        result[i] = data[i] ^ key_bytes[i % len(key_bytes)]
    return bytes(result)

def encrypt_password(password: str) -> str:
    """
    Encrypts a password using the requested pipeline:
    1. URL Safe Base64 Encode
    2. Gzip Compress
    3. Cycled XOR Encrypt
    """
    # 1. URL safe base64 encoded
    b64_encoded = base64.urlsafe_b64encode(password.encode('utf-8'))
    # 2. Gzipped
    gzipped = zlib.compress(b64_encoded)
    # 3. Cycled XOR encrypted
    xor_result = cycled_xor_bytes(gzipped, XOR_KEY)
    # We must return a string to store in JSON. 
    # 'latin-1' maps bytes 1:1 to characters, ensuring no data loss.
    return xor_result.decode('latin-1')

def decrypt_password(encrypted_str: str) -> str:
    """
    Decrypts a password from the JSON file.
    """
    # Recover bytes from string
    encrypted_bytes = encrypted_str.encode('latin-1')
    # Reverse 3. XOR
    xor_result = cycled_xor_bytes(encrypted_bytes, XOR_KEY)
    # Reverse 2. Gunzip
    gunzipped = zlib.decompress(xor_result)
    # Reverse 1. Base64 decode
    decoded = base64.urlsafe_b64decode(gunzipped)
    return decoded.decode('utf-8')

# ---------------------------

def mainMenu():
    login_info_path = "login_info.json"
    loggedIn = False

    print("\nWelcome to the GD Python Main Menu!\n")

    def login_procedure():
        nonlocal loggedIn
        login_info = {}
        
        # Check if file exists
        if os.path.exists(login_info_path):
            try:
                with open(login_info_path, 'r') as f:
                    content = f.read().strip()
                    if content:
                        # File exists and has content, load it
                        login_info = json.loads(content)
                        username = login_info.get("username", "")
                        encrypted_pass = login_info.get("password", "")
                        
                        if username and encrypted_pass:
                            # Decrypt the password for use in this session
                            decrypted_pass = decrypt_password(encrypted_pass)
                            login_info["password"] = decrypted_pass
                            
                            loggedIn = True
                            print(f"Logged in as: {username} from previous session(s).")
                            return login_info
            except Exception as e:
                print(f"Error reading login file: {e}")

        # If we are here, file doesn't exist, is empty, or is invalid
        print("Seems like you are \033[1;31;40mnot logged in\033[0m.\nWould you like to \033[1;32;40mlog in\033[0m?")
        choice = input("Enter 'y' to log in or 'n' to continue without logging in: ").strip().lower()
        
        if choice == 'y':
            usernameLogin = input("Enter your username: ")
            passwordLogin = getpass.getpass("Enter your password: ")
            
            # Encrypt the password before storing
            encrypted_password = encrypt_password(passwordLogin)
            
            # Prepare dictionary for saving
            save_data = {"username": usernameLogin, "password": encrypted_password}
            
            try:
                with open(login_info_path, 'w') as f:
                    json.dump(save_data, f)
                
                # Return the decrypted password for immediate use
                login_info = {"username": usernameLogin, "password": passwordLogin}
                loggedIn = True
                print(f"Logged in as: {usernameLogin}.")
            except Exception as e:
                print(f"An error occurred while saving login info: {e}")
                # Even if saving fails, allow session to continue
                login_info = {"username": usernameLogin, "password": passwordLogin}
        else:
            print("Continuing without logging in.")
            
        return login_info

    login_info = login_procedure()

    print("\nPlease choose an option from the menu below:\n")
    print("1. Search for Online Levels")
    print("2. Download Level Data by ID")
    print("3. Upload a comment to an account")
    print("4. Upload a comment to a level")
    print("5. Decode your save file")
    print("6. Like a GD Item")
    print("7: Get Comments from a Level")
    print("8: Get a user's profile")
    print("9. Get your friends list or blocked list (requires login)\n")
    
    def input_int(prompt, min_value=None, max_value=None):
        while True:
            try:
                val = int(input(prompt))
            except ValueError:
                print("Please enter a valid integer.")
                continue
            if min_value is not None and val < min_value:
                print(f"Value must be >= {min_value}")
                continue
            if max_value is not None and val > max_value:
                print(f"Value must be <= {max_value}")
                continue
            return val

    if loggedIn:
        # Fetch IDs if logged in
        userIDLogin, accountIDLogin = getLoginInfo.getAccountInfoFromLogin(login_info.get("username", ""))
        passwordLogin = login_info.get("password", "")
    else:
        userIDLogin, accountIDLogin = None, None
        passwordLogin = None

    choice = input_int("Enter the number of your choice (or select 0 to quit): ")

    if choice == 0:
        return False
    
    elif choice == 1:
        searchString = input("Enter search string (leave blank for none): ")
        if searchString:
            search_type = 0
        else:
            search_type = input_int("Enter search type\n(https://wyliemaster.github.io/gddocs/#/endpoints/levels/getGJLevels21 for all the info): ")
        star = input_int("Enter star rated (0 for not rated, 1 for rated): ")
        print(levelSearch.getGJLevels(search_type, searchString, star))

    elif choice == 2:
        levelID = input_int("Enter the Level ID: ")
        print(levelData.reqLevelData(levelID))

    elif choice == 3:
        if not loggedIn:
            print("\033[1;31;40mError\033[0m: You must be logged in to upload an account comment.")
            return True
        accountID = accountIDLogin
        comment = input("Enter your comment: ")
        password = passwordLogin
        print(uploadComment.uploadGJAccComment20(accountID, password, comment))

    elif choice == 4:
        if not loggedIn:
            print("\033[1;31;40mError\033[0m: You must be logged in to upload a level comment.")
            return True
        levelID = input_int("Enter the Level ID: ")
        userName = login_info.get("username", "")
        comment = input("Enter your comment: ")
        percentage = input_int("Enter percentage completed (0-100): ", 0, 100)
        password = passwordLogin
        print(uploadLevelComment.uploadGJComment21(userName, comment, levelID, percentage, password))

    elif choice == 5:
        filePath = input("Enter the path to your Geometry Dash save file: ")
        print(decryptSave.decryptGDSaveFile(filePath))

    elif choice == 6:
        itemID = input_int("Enter the Item ID: ")
        type = input_int("Enter the type (1 for level, 2 for level comment, 3 for account comment, 4 for level list): ")
        print(likeItem.likeGJItem211(itemID, type))

    elif choice == 7:
        levelID = input_int("Enter the Level ID: ")
        page = input_int("Enter the page number: ")
        mode = input_int("Enter the mode (0 for most recent, 1 for most liked): ")
        getComments.getGJComments21(levelID, page, mode)

    elif choice == 8:
        userName = input("Enter the searchString: ")
        getProfile.getGJUsers20(userName, 0)

    elif choice == 9:
        if not loggedIn:
            print("\033[1;31;40mError\033[0m: You must be logged in to get your friends or blocked list.")
            return True
        list_type = input_int("Enter 0 for friends list or 1 for blocked list: ")
        getUserList.getGJUserList20(accountIDLogin, passwordLogin, list_type)
    
    restart_choice = input("Do you want to run the program again? (y/n): ")
    if restart_choice.lower() == 'y':
        return True
    else:
        logout = input("Do you want to log out? (y/n): ")
        if logout.lower() == 'y':
            try:
                with open(login_info_path, 'w') as f:
                    json.dump({}, f) # Overwrite with empty JSON object
                print("Logged out successfully.")
                return False
            except Exception as e:
                print(f"An error occurred while logging out: {e}")
                
        else:
            return False

while mainMenu():
    print("\nRestarting...\n")

print("Program terminated. Thanks for using.\n")
start_time = time.time()
print("Exiting in 3 seconds...")
time.sleep(3 - (time.time() - start_time))
sys.exit(0)

if __name__ == "__main__":
    print("Starting program mainMenu.py...")
    mainMenu()