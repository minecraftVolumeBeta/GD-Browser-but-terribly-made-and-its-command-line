import requests
import base64
import pandas as pd

commentAttributes = [
    {"key": 1, "name": "levelID"},
    {"key": 2, "name": "comment"},
    {"key": 3, "name": "authorPlayerID"},
    {"key": 4, "name": "likes"},
    {"key": 5, "name": "dislikes"},
    {"key": 6, "name": "messageID"},
    {"key": 7, "name": "spam"},
    {"key": 8, "name": "authorAccountID"},
    {"key": 9, "name": "age"},
    {"key": 10, "name": "percent"},
    {"key": 11, "name": "modBadge"},
    {"key": 12, "name": "moderatorChatColor"}
]

authorAttributes = [
    {"key": 1, "name": "userName"},
    {"key": 9, "name": "icon"},
    {"key": 10, "name": "playerColor"},
    {"key": 11, "name": "playerColor2"},
    {"key": 14, "name": "iconType"},
    {"key": 15, "name": "glow"},
    {"key": 16, "name": "accountID"}
]

def getGJComments21(levelID: int = 0, page: int = 1, mode: int = 0):
    data = {
        "levelID": levelID,
        "page": page,
        "mode": mode,
        "secret": "Wmfd2893gb7"
    }
    headers = {
        "User-Agent": "",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    request = requests.post("http://www.boomlings.com/database/getGJComments21.php", headers=headers, data=data).text
    all_comments_data = []
    request = request.split('#')[0]
    for entry in request.split('|'):
        comments_data, authors_data = parse_comments(entry)
        if comments_data and authors_data:
            all_comments_data.append((comments_data, authors_data))

    print("\n\n")
    for comments_data, authors_data in all_comments_data:
        print("Comment Part:")
        print(", ".join(f"{k}: {v}" for k, v in comments_data.items()))
        
        print("Author Part:")
        print(", ".join(f"{k}: {v}" for k, v in authors_data.items()))
        
        print("-" * 40)

def parse_comments(data_strings):
    if ':' not in data_strings:
        return {}
    
    commentPart, authorPart = data_strings.split(':', 1)
    comments_data = []
    authors_data = []

    commentPartArr = commentPart.split('~')
    for i in range(0, len(commentPartArr), 2):
        if i + 1 < len(commentPartArr):
            key = commentPartArr[i]
            value = commentPartArr[i + 1]
            attr_name = next((attr["name"] for attr in commentAttributes if attr["key"] == int(key)), None)

            if attr_name:
                if key in ['1', '3', '4', '5', '6', '8', '10', '11']:
                    value = int(value) if value else None
                elif key in ['9', '12']:
                    value = str(value) if value else None
                elif key == '2':
                    value = ("\"" +(base64.urlsafe_b64decode(value).decode('utf-8') if value else None) + "\"")
                elif key == '7':
                    value = bool(int(value)) if value else None
                
                comments_data.append((attr_name, value))

    authorPartArr = authorPart.split('~')
    for i in range(0, len(authorPartArr), 2):
        if i + 1 < len(authorPartArr):
            key = authorPartArr[i]
            value = authorPartArr[i + 1]
            attr_name = next((attr["name"] for attr in authorAttributes if attr["key"] == int(key)), None)

            if attr_name:
                if key == '1':
                    value = str(value) if value else None
                elif key in ['9', '10', '11', '14', '15', '16']:
                    value = int(value) if value else None
                
                authors_data.append((attr_name, value))

    return dict(comments_data), dict(authors_data)