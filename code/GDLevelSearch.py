import requests
import base64
import urllib.parse

def parseSongData(song_string: str = ""):
    """
    Parses a single song string from the response (format: key~|~value~|~...)
    """
    song_attributes = {
        1: "ID",
        2: "Name",
        3: "ArtistID",
        4: "ArtistName",
        5: "Size (MB)",
        6: "VideoID",
        7: "YoutubeURL",
        8: "IsVerified",
        9: "Priority",
        10: "DownloadLink",
        11: "NongEnum",
        12: "ExtraArtistIDs",
        13: "IsNew",
        14: "NewType",
        15: "ExtraArtistNames"
    }
    
    song_info = {}
    parts = song_string.split('~|~')
    
    for i in range(0, len(parts), 2):
        if i + 1 >= len(parts):
            break
        
        try:
            key = int(parts[i])
            value = parts[i+1]
        except ValueError:
            continue

        if key in song_attributes:
            label = song_attributes[key]
            
            if key in [1, 3, 9, 11, 14]:
                song_info[label] = int(value)
            elif key == 13:
                song_info[label] = bool(int(value))
            elif key == 8:
                value = value.rstrip('~')
                song_info[label] = bool(int(value))
            elif key == 5:
                song_info[label] = float(value)
            elif key in [7, 10]:
                if key == 7:
                    song_info[label] = "https://www.youtube.com/channel/" + urllib.parse.unquote(value)
                else:
                    song_info[label] = urllib.parse.unquote(value)
            else:
                song_info[label] = value

    return song_info

def parseLevelData(levelString: str = ""):
    attributes = {
        1: "levelID", 2: "levelName", 3: "description", 5: "version", 6: "playerID",
        8: "difficultyDenominator", 9: "difficultyNumerator", 10: "downloads", 11: "setCompletes",
        12: "officialSong", 13: "gameVersion", 14: "likes", 15: "length", 16: "dislikes",
        17: "demon", 18: "stars", 19: "featureScore", 25: "auto", 26: "recordString",
        27: "password", 28: "uploadDate", 29: "updateDate", 30: "copiedID", 31: "twoPlayer",
        35: "customSongID", 36: "extraString", 37: "coins", 38: "verifiedCoins",
        39: "starsRequested", 40: "lowDetailMode", 41: "dailyNumber", 42: "epic",
        43: "demonDifficulty", 44: "isGauntlet", 45: "objects", 46: "editorTime",
        47: "editorTimeCopies", 48: "settingsString", 52: "songIDs", 53: "sfxIDs",
        54: "unknown", 57: "verificationTime"
    }
    result = {}
    parts = levelString.split(":")
    
    for i in range(0, len(parts) - 1, 2):
        key_str = parts[i]
        value = parts[i + 1] if i + 1 < len(parts) else None
        
        try:
            key = int(key_str)
        except ValueError:
            continue

        if value:
            if key == 3:
                try:
                    value = base64.urlsafe_b64decode(value).decode('utf-8', errors='ignore')
                except Exception:
                    pass

            if key in [17, 25, 31, 38, 44]:
                value = bool(int(value))
            elif key == 35:
                value = int(value.split('#')[0], 10)
            elif key in {1, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15,
                          16, 18, 19, 30, 37, 39, 42, 43, 45,
                          46, 47, 57}:
                try:
                    value = int(value)
                except ValueError:
                    value = None

            result[attributes.get(key, str(key))] = value
        else:
            result[attributes.get(key, str(key))] = None

    return result

def printLevelData(level_data):

    if not level_data:
        return

    print(f"{'Key':<25}{'Value':<50}")
    print("=" * 75)
    
    sorted_keys = sorted(level_data.keys())
    priority_keys = ["levelName", "levelID", "description"]
    
    for key in priority_keys:
        value = level_data[key]
        
        if value is None:
            continue

        if isinstance(value, bool):
            val_str = "Yes" if value else "No"
        elif value == "":
            val_str = "N/A"
        else:
            val_str = str(value)
            
        print(f"{key:<25}{val_str:<50}")
        
    for key in sorted_keys:
        value = level_data[key]
        
        if value is None:
            continue

        if isinstance(value, bool):
            val_str = "Yes" if value else "No"
        elif value == "":
            val_str = "N/A"
        else:
            val_str = str(value)
        if key not in priority_keys:
            print(f"{key:<25}{val_str:<50}")

    print("=" * 75)

def getGJLevels(searchType = "", searchString = "", star = 0):
    data = {
        "str": searchString,
        "type": searchType,
        "star": star,
        "secret": "Wmfd2893gb7"
    }
    headers = {
        "User-Agent": "",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    request = requests.post("http://www.boomlings.com/database/getGJLevels21.php", headers=headers, data=data)
    
    if not request.text or request.text == "-1":
        print("No levels found.")
        return

    response_parts = request.text.split('#')

    levels_str = response_parts[0] if len(response_parts) > 0 else ""
    creators_str = response_parts[1] if len(response_parts) > 1 else ""
    songs_str = response_parts[2] if len(response_parts) > 2 else ""
    page_str = response_parts[3] if len(response_parts) > 3 else ""
    response_hash = response_parts[4] if len(response_parts) > 4 else ""

    # 1. Page Info
    print("\n--- PAGE INFO ---")
    if page_str:
        p_info = page_str.split(':')
        print(f"Total Levels: {p_info[0] if len(p_info) > 0 else 'N/A'}")
        print(f"Page Offset: {p_info[1] if len(p_info) > 1 else 'N/A'}")
        print(f"Amount: {p_info[2] if len(p_info) > 2 else 'N/A'}")
    else:
        print("No page info available.")
    
    # 2. Creators
    print("\n--- CREATORS ---")
    if creators_str:
        for creator in creators_str.split('|'):
            c_parts = creator.split(':')
            if len(c_parts) >= 3:
                print(f"User: {c_parts[1]} | User ID: {c_parts[0]} | Account ID: {c_parts[2]}")
    else:
        print("No creator data.")

    # 3. Songs
    print("\n--- SONGS ---")
    if songs_str:

        song_list = songs_str.split(':')
        
        for song in song_list:
            if not song.strip():
                continue
            
            song_data = parseSongData(song)
            
            if song_data:

                header_id = song_data.get("ID", "Unknown Song")
                print(f"Song ID: {header_id}")
                print("-" * 40)
                
                sorted_keys = sorted(song_data.keys())
                for key in sorted_keys:
                    if key != "ID":
                        val = song_data[key]
                        if val is not None and val != "":
                            print(f"{key}: {val}")
                print("-" * 40)
    else:
        print("No custom song data.")

    print("\n--- HASH ---")
    print(f"Response Hash: {response_hash}")
    # 4. Levels
    print("\n--- LEVELS ---")
    individualLevels = levels_str.split("|")
    for level in individualLevels:
        if level.strip():
            printLevelData(parseLevelData(level))