import requests
import base64
import zlib
import readJSON as readJson
import decryptGDSaveFile as decryptLevel
import levelAnalysis
import analyzeJsonLevel as analyzeJson
import os
import xor
import json

def getLevelData(response: str = "", levelID: int = 0):
    # Separate the hash from the data
    # The response usually ends with #hash1#hash2
    if '#' in response:
        removed_hash = response.split('#')[0]
    else:
        removed_hash = response

    parts = removed_hash.split(':')
    
    # Initialize levelName to avoid errors if key 2 is missing or out of order
    levelName = "Unknown Level"
    levelString = ""
    
    # Dictionary to store parsed data for returning
    parsed_data = {}

    # Mapping for general level info
    attributes = {
        1: "levelID", 2: "levelName", 3: "description", 4: "levelString",
        5: "version", 6: "playerID", 8: "difficultyDenominator", 9: "difficultyNumerator",
        10: "downloads", 11: "setCompletes", 12: "officialSong", 13: "gameVersion",
        14: "likes", 15: "length", 16: "dislikes", 17: "demon", 18: "stars",
        19: "featureScore", 25: "auto", 26: "recordString", 27: "password",
        28: "uploadDate", 29: "updateDate", 30: "copiedID", 31: "twoPlayer",
        35: "customSongID", 36: "extraString", 37: "coins", 38: "verifiedCoins",
        39: "starsRequested", 40: "lowDetailMode", 41: "dailyNumber", 42: "epic",
        43: "demonDifficulty", 44: "isGauntlet", 45: "objects", 46: "editorTime",
        47: "editorTimeCopies", 48: "settingsString", 52: "songIDs", 53: "sfxIDs",
        54: "unknownValue", 55: "verificationTime"
    }

    for i in range(0, len(parts)-1, 2):
        key_str = parts[i]
        value = parts[i+1] if i+1 < len(parts) else None

        try:
            key = int(key_str)
        except ValueError:
            continue

        if value:
            # Check if key requires string conversion
            if key in [2, 3, 4, 26, 27, 28, 29, 36, 48]:
                try:
                    value = str(value)
                except ValueError:
                    pass
                
                if key == 2:
                    levelName = value
                    parsed_data["levelName"] = value
                elif key == 3:
                    # Decode Base64 Description
                    try:
                        # Added errors='replace' to handle potential encoding issues
                        value = base64.urlsafe_b64decode(value.encode()).decode('utf-8', errors='replace')
                    except Exception:
                        pass # Keep raw if decoding fails
                    parsed_data["description"] = value
                elif key == 4:
                    # --- LEVEL STRING DECOMPRESSION LOGIC ---
                    # 1. 'value' is a Base64 encoded string.
                    # 2. Decode Base64 -> Returns RAW BYTES (Compressed Gzip Data).
                    #    This data is non-UTF-8 binary.
                    print("Decoding Base64...")
                    raw_compressed_bytes = base64.urlsafe_b64decode(value)
                    
                    # 3. Decompress Gzip -> Returns RAW BYTES (The Level Data String).
                    print("Decompressing Gzip...")
                    decompressed_bytes = zlib.decompress(raw_compressed_bytes, 15 | 32)
                    
                    # 4. Decode final bytes to String.
                    # 'errors="replace"' ensures that if any binary artifacts exist 
                    # after decompression, they don't crash the script.
                    levelString = decompressed_bytes.decode('utf-8', errors='replace')
                    print("Decompression successful.")
                    
                    parsed_data["levelString"] = levelString

                    # Trigger analysis immediately when we get the level string
                    print(f"Parsing level: {levelName}")
                    levelAnalysis.analyzeLevelData(levelString, levelID)
                    
                elif key == 27:
                    # Decrypt password
                    value = xor.cycled_xor(value, "26364")
                    parsed_data["password"] = value
                elif key == 52:
                    # Parse Song IDs
                    songIDs = value.split(',')
                    value = {f"Song {i}": songIDs[i] if i < len(songIDs) else None for i in range(len(songIDs))}
                    parsed_data["songIDs"] = value
                elif key == 53:
                    # Parse SFX IDs
                    sfxIDs = value.split(',')
                    value = {f"SFX {i}": sfxIDs[i] if i < len(sfxIDs) else None for i in range(len(sfxIDs))}
                    parsed_data["sfxIDs"] = value
            else:
                # Store other attributes
                attr_name = attributes.get(key)
                if attr_name:
                    parsed_data[attr_name] = value
    
    return parsed_data

def requestData(levelID: int = 0):
    if levelID is None:
        print("No level ID input! Please input a level ID!")
        return None
    
    data = {
        "levelID": levelID,
        "secret": "Wmfd2893gb7"
    }
    headers = {
        "User-Agent": "",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    while True:
        print("Downloading level data...")
    
        try:
            req = requests.post("http://www.boomlings.com/database/downloadGJLevel22.php", headers=headers, data=data).text
        except Exception as e:
            print(f"Request failed: {e}")
            return None

        # Check for error codes
        if req == "-1":
            print("Level not found.")
            return None
        if req == "" or req is None:
            print("Empty response.")
            return None

        analyze = input("Analyze level data? (y/n): ").lower()
        if analyze == "y":
            # Now returns the parsed data instead of None
            getLevelData(req, levelID)
        else:
            # Even if not analyzing 'interactively', we parse to return the data
            return getLevelData(req, levelID)

def reqLevelData(levelID):
    path_to_json = "savedLevelsAsJson"
    filename = f"{levelID}_levelAnalysis.json"
    filePath = os.path.join(path_to_json, filename)
    
    if os.path.exists(filePath):
        analyze = input("Level analysis JSON found locally. Re-analyze? (y/n): ").lower()
        if analyze == "y":
            print(f"Using existing analysis at {filePath}")
            analyzeJson.analyzeJsonLevel(True, filePath)
            # Return the JSON data to ensure the function doesn't return None
            try:
                with open(filePath, 'r') as f:
                    return True
            except Exception as e:
                print(f"Could not read local JSON: {e}")
                return None
        else:
            os.remove(filePath)
            print("Existing analysis deleted. Fetching fresh data...")
            # Return the result of requestData
            requestData(levelID)

    else:
        print("Level analysis JSON not found locally. Fetching fresh data...")
        # Return the result of requestData
        requestData(levelID)