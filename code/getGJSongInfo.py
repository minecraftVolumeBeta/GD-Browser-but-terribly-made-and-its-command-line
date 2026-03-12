import requests
import urllib

def getGJSongInfo(songID: int):
    data = {
        "songID": songID,
        "secret": "Wmfd2893gb7"
    }
    headers = {
        "User-Agent": "",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    req = requests.post("http://www.boomlings.com/database/getGJSongInfo.php", headers=headers, data=data).text
    if not req or req == "-1":
        print("Song not found.")
        return None
    print()
    print(parseSongInfo(req))

def parseSongInfo(song_string: str):
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
                try:
                    song_info[label] = bool(int(value))
                except ValueError:
                    song_info[label] = value
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