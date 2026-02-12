import requests

def getGJUserInfo20(accountID: int):
    data = {
        "targetAccountID": accountID,
        "secret": "Wmfd2893gb7"
    }
    headers = {
        "User-Agent": "",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        request = requests.post("http://www.boomlings.com/database/getGJUserInfo20.php", headers=headers, data=data).text
    except Exception as e:
        print(f"Request failed: {e}")
        return

    if request == "-1" or not request:
        print("User not found or error occurred.")
        return
    
    fullData = parseuserInfo(request)

    priority_keys = ["userName", "accountID", "userID", "classicLevels", "platformerLevels", "demons", "stars", "moons", "diamonds", "creatorPoints", "ranking", "youTube", "twitch", "twitter", "isRegistered", "modLevel"]

    for key in priority_keys:
        if key in fullData:
            print(f"{key}: {fullData[key]}")
            print("-" * 40)

    print("-" * 40)

    for key in sorted(fullData.keys()):
        if key not in priority_keys:
            print(f"{key}: {fullData[key]}")
            print("-" * 40)

    for key in sorted(fullData.keys()):
        if key == "accountID" and fullData[key] == 71:
            print("\nSide note: this user is literally \033[1;36;40mRobTop\033[0m, the \033[1;32;40mcreator\033[0m of the \033[1;33;40mgame\033[0m!\n")


def parseuserInfo(data_string):
    user_profile_keys = {
        1: "userName",
        2: "userID",
        3: "stars",
        4: "demons",
        6: "ranking",
        7: "accountHighlight",
        8: "creatorPoints",
        9: "iconID",
        10: "color",
        11: "color2",
        13: "secretCoins",
        14: "iconType",
        15: "special",
        16: "accountID",
        17: "usercoins",
        18: "messageState",
        19: "friendsState",
        20: "youTube",
        21: "accIcon",
        22: "accShip",
        23: "accBall",
        24: "accBird",
        25: "accDart(wave)",
        26: "accRobot",
        27: "accStreak",
        28: "accGlow",
        29: "isRegistered",
        30: "globalRank",
        31: "friendRequestState",
        38: "messages",
        39: "friendRequests",
        40: "newFriends",
        41: "NewFriendRequest",
        42: "age",
        43: "accSpider",
        44: "twitter",
        45: "twitch",
        46: "diamonds",
        48: "accExplosion",
        49: "modLevel",
        50: "commentHistoryState",
        51: "color3",
        52: "moons",
        53: "accSwing",
        54: "accJetpack",
        55: "demons",
        56: "classicLevels",
        57: "platformerLevels"
    }
    demonFormat = [
        "easyDemon",
        "mediumDemon",
        "hardDemon",
        "insaneDemon",
        "extremeDemon",
        "easyPlatformerDemon",
        "mediumPlatformerDemon",
        "hardPlatformerDemon",
        "insanePlatformerDemon",
        "extremePlatformerDemon"
    ]
    classicLevelsFormat = [
        "auto",
        "easy",
        "normal",
        "hard",
        "harder",
        "insane",
        "daily",
        "gauntlet"
    ]
    platformerLevelsFormat = [
        "auto",
        "easy",
        "normal",
        "hard",
        "harder",
        "insane"
    ]
    user_info = {}

    parts = data_string.split(':')
    for i in range(0, len(parts), 2):
        if i + 1 >= len(parts):
            break
        try:
            key = int(parts[i])
            value = parts[i + 1]
        except ValueError:
            continue
        if key in user_profile_keys:
            if key in [1, 20, 42, 44, 45]:
                final_val = str(value) if value else None
                if key == 20 and final_val:
                    final_val = f"https://www.youtube.com/channel/{final_val}"
                elif key == 44 and final_val:
                    final_val = f"https://x.com/{final_val}"
                elif key == 45 and final_val:
                    final_val = f"https://www.twitch.tv/{final_val}"
                user_info[user_profile_keys[key]] = final_val
            elif key == 41:
                user_info[user_profile_keys[key]] = bool(int(value)) if value else None
            elif key in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 43, 46, 47, 48, 49, 50, 51, 52, 53, 54]:
                user_info[user_profile_keys[key]] = int(value) if value else None
                if key == 29:
                    if user_info[user_profile_keys[key]] == 1:
                        user_info[user_profile_keys[key]] = "\033[1;32;40mYes\033[0m"
                    elif user_info[user_profile_keys[key]] == 0:
                        user_info[user_profile_keys[key]] = "\033[1;31;40mNo\033[0m"
                elif key == 18:
                    if user_info[user_profile_keys[key]] == 0:
                        user_info[user_profile_keys[key]] = "\033[1;32;40mAnyone\033[0m can message this user."
                    elif user_info[user_profile_keys[key]] == 1:
                        user_info[user_profile_keys[key]] = "Only this user's \033[1;33;40mfriends\033[0m can message this user."
                    elif user_info[user_profile_keys[key]] == 2:
                        user_info[user_profile_keys[key]] = "\033[1;31;40mNo one\033[0m can message this user."
                elif key == 19:
                    if user_info[user_profile_keys[key]] == 0:
                        user_info[user_profile_keys[key]] = "\033[1;32;40mAnyone\033[0m can friend request this user."
                    elif user_info[user_profile_keys[key]] == 1:
                        user_info[user_profile_keys[key]] = "\033[1;31;40mNo one\033[0m can friend request this user."
                elif key == 49:
                    if user_info[user_profile_keys[key]] == 0:
                        user_info[user_profile_keys[key]] = "This user is\033[1;31;40m not\033[0m a\033[1;33;40m Moderator\033[0m."
                    elif user_info[user_profile_keys[key]] == 1:
                        user_info[user_profile_keys[key]] = "This user \033[1;32;40mis\033[0m a\033[1;33;40m Moderator\033[0m!"
                    elif user_info[user_profile_keys[key]] == 2:
                        user_info[user_profile_keys[key]] = "This user \033[1;32;40mis\033[0m an\033[1;35;40m Elder Moderator\033[0m!"

        if key == 55:
            if value:
                demons = value.split(',')
                user_info["demons"] = {demonFormat[i]: int(demons[i]) if i < len(demons) else 0 for i in range(len(demonFormat))}
        elif key == 56:
            if value:
                classicLevels = value.split(',')
                user_info["classicLevels"] = {classicLevelsFormat[i]: int(classicLevels[i]) if i < len(classicLevels) else 0 for i in range(len(classicLevelsFormat))}
        elif key == 57:
            if value:
                platformerLevels = value.split(',')
                user_info["platformerLevels"] = {platformerLevelsFormat[i]: int(platformerLevels[i]) if i < len(platformerLevels) else 0 for i in range(len(platformerLevelsFormat))}
        else:
            continue
    return user_info