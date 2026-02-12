import json
import base64
import gzip
import os
import sys

def analyzeJsonLevel(recieved: bool = True, filepath: str = "levelData.json"):
    # --- SETUP OUTPUT FILE ---
    output_dir = "savedAnalysis"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = os.path.basename(filepath)
    level_id = filename.split('_')[0]
    
    output_filename = f"{level_id}_analysis.txt"
    output_path = os.path.join(output_dir, output_filename)
    
    print(f"Reading JSON from {filepath}...")

    data = None
    try:
        # Explicitly use UTF-8 to match the writer
        with open(filepath, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print(f"File {filepath} not found.")
        return
    except json.JSONDecodeError as e:
        print(f"\n[CRITICAL ERROR] The JSON file is corrupt or truncated.")
        print(f"Error: {e.msg}")
        print(f"Location: Line {e.lineno}, Column {e.colno}")
        print(f"\nThis usually happens because the file write was interrupted previously.")
        print(f"Please delete '{filepath}' and re-run the download to generate a fresh file.")
        return
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return

    print(f"Writing analysis to {output_path}...")

    with open(output_path, 'w', encoding='utf-8') as f:
        # Mapping of Object IDs to Names
        objectIDs = {
            "portals": {
                "12": "cube", "13": "ship", "47": "ball", "111": "ufo", "660": "wave",
                "745": "robot", "1331": "spider", "45": "mirrorOn", "46": "mirrorOff",
                "101": "mini", "99": "big", "286": "dual", "287": "single", "200": "-1x",
                "201": "1x", "202": "2x", "203": "3x", "1334": "4x"
            },
            "coins": {
                "1329": "coin"
            },
            "orbs": {
                "36": "yellow", "84": "blue", "141": "pink", "1022": "green",
                "1333": "red", "1330": "black", "1704": "greenDash", "1751": "pinkDash",
                "1594": "trigger"
            },
            "triggers": {
                "29": "Color", "30": "Color", "31": "StartPos", "32": "EnableTrail",
                "33": "DisableTrail", "34": "StartPos2", "104": "Color", "105": "Color",
                "221": "Color", "717": "Color", "718": "Color", "743": "Color",
                "744": "Color", "899": "Color", "900": "Color", "915": "Color",
                "901": "Move", "1006": "Pulse", "1007": "Alpha", "1049": "Toggle",
                "1268": "Spawn", "1346": "Rotate", "1347": "Follow", "1520": "Shake",
                "1585": "Animate", "1595": "Touch", "1611": "Count", "1612": "HidePlayer",
                "1613": "ShowPlayer", "1616": "Stop", "1811": "InstantCount",
                "1812": "OnDeath", "1814": "FollowPlayerY", "1815": "Collision",
                "1817": "Pickup", "1818": "BGEffectOn", "1819": "BGEffectOff",
                "22": "Transition1", "24": "Transition2", "23": "Transition3",
                "25": "Transition4", "26": "Transition5", "27": "Transition6",
                "28": "Transition7", "55": "Transition8", "56": "Transition9",
                "57": "Transition10", "58": "Transition11", "59": "Transition12",
                "1912": "Random", "1913": "CameraZoom", "1914": "CameraStatic",
                "1916": "CameraOffset", "1917": "Reverse", "1931": "LevelEnd",
                "1932": "StopJump", "1934": "Song", "1935": "TimeWarp",
                "2015": "CameraRotate", "2016": "CameraGuide", "2062": "CameraEdge",
                "2067": "Scale", "2068": "AdvRandom", "2701": "Pause", "2702": "Resume"
            },
            "misc": {
                "spikes": ["Spikes", 8, 9, 10, 11, 39, 103, 104, 144, 145, 175, 176, 177, 178, 179, 217, 218, 458, 459, 241],
                "saws": ["Saws", 1705, 740, 1619, 1706, 741, 742, 1620, 184, 1707, 1734, 678, 185, 1708, 1736, 187, 679, 1709, 1710, 186, 1735, 188, 680, 183],
                "invisibles": ["Fading", 146, 147, 206, 204, 673, 674, 1340, 1341, 1342, 1343, 1344, 1345, 144, 205, 145, 459, 740, 741, 742],
                "pickups": ["Pickups", 1614, 1598, 1587, 1275],
                "texts": ["Text", 914, 1615],
                "glows": ["Glow", 1888, 1763, 1762, 1293, 1270, 1269, 1012, 1013, 1011, 1886, 1759, 1758, 1291, 1274, 1273, 504, 505, 503, 1887, 1761, 1760, 1272, 1271, 1009, 1010, 1292],
                "hands": ["Hands", 1844, 1845, 1846, 1847, 1848],
                "pulses": ["Pulsing", 50, 52, 51, 53, 54, 60, 148, 149, 405, 132, 460, 494, 133, 136, 150, 236, 497, 495, 496, 15, 16, 17],
                "breakables": ["Breakable", 143],
                "collisions": ["Collisions", 1816],
                "pixels": ["Pixels", 916, 917],
                "clouds": ["Clouds", 936, 937, 938, 129, 130, 131],
                "arrows": ["Arrows", 1768, 1766, 1603, 1844, 132, 494, 460],
                "particles": ["Particles", 1586, 1700, 1519, 1618],
                "monsters": ["Monsters", 918, 1327, 1328, 1584],
                "fires": ["Fire", 920, 923, 924, 921],
                "defaultBlock": ["Default Block", 1]
            }
        }

        # 1. Build a Master ID Map
        ID_LOOKUP_MAP = {}
        for cat, mapping in objectIDs.items():
            if cat == "misc":
                for subcat, ids in mapping.items():
                    for i in range(1, len(ids)):
                        ID_LOOKUP_MAP[str(ids[i])] = subcat
            else:
                for id_str, name in mapping.items():
                    ID_LOOKUP_MAP[str(id_str)] = name

        objectList = data.get("Level Objects", [])

        if not objectList:
            f.write("No objects found.\n")
            return

        f.write(f"Analyzing {len(objectList)} objects...\n\n")

        frequentObjects = {}

        for obj in objectList:
            obj_id = str(obj.get("1"))
            
            if not obj_id:
                continue

            if obj_id in ID_LOOKUP_MAP:
                obj_name = ID_LOOKUP_MAP[obj_id]
            else:
                obj_name = f"ID {obj_id}"

            frequentObjects[obj_name] = frequentObjects.get(obj_name, 0) + 1

        f.write("Frequent Objects in Level (All IDs):\n\n")
        for obj_name, count in sorted(frequentObjects.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{obj_name}: {count}\n")
            f.write("-" * 30 + "\n")
        
        f.write("\n\nAnalyzing Specific Objects of Interest:\n\n")

        # --- Portals ---
        portals = []
        for obj in objectList:
            obj_id = str(obj.get("1"))
            xPos = str(obj.get("2"))
            yPos = str(obj.get("3"))
            
            if obj_id in objectIDs["portals"]:
                portals.append(objectIDs["portals"][obj_id] + f" (X: {xPos}, Y: {yPos})")
        
        if portals:
            f.write("\nPortals in Level:\n\n")
            for portal in portals:
                f.write(f"{portal}\n")
                f.write("-" * 30 + "\n")
        else:
            f.write("No Portals found or all are unknown IDs.\n")

        # --- Triggers ---
        triggers = []
        for obj in objectList:
            obj_id = str(obj.get("1"))
            xPos = str(obj.get("2"))
            yPos = str(obj.get("3"))
            targetGroupID = str(obj.get("51"))
            
            if obj_id in objectIDs["triggers"]:
                triggers.append(objectIDs["triggers"][obj_id] + f" (X: {xPos}, Y: {yPos}), targetGroupID: {targetGroupID}")
        
        if triggers:
            f.write("\nTriggers in Level:\n\n")
            for trigger in triggers:
                f.write(f"{trigger}\n")
                f.write("-" * 30 + "\n")

            f.write("\nMost targeted groupIDs (From Triggers only):\n\n")
            targetCount = {}
            for obj in objectList:
                obj_id = str(obj.get("1"))
                targetGroupID = str(obj.get("51"))
                
                if obj_id in objectIDs["triggers"] and targetGroupID and targetGroupID != "0" and targetGroupID != "None":
                    targetCount[targetGroupID] = targetCount.get(targetGroupID, 0) + 1
            
            if targetCount:
                for targetGroupID, count in sorted(targetCount.items(), key=lambda x: x[1], reverse=True):
                    f.write(f"GroupID {targetGroupID}: targeted {count} times\n")
            else:
                f.write("No trigger targets found.\n")

        #text objects
        texts = []
        for obj in objectList:
            obj_id = str(obj.get("1"))
            xPos = str(obj.get("2"))
            yPos = str(obj.get("3"))
            textContentUndecoded = str(obj.get("31", ""))
            try:
                textContentB64 = base64.urlsafe_b64decode(textContentUndecoded.encode()).decode()
                textContent = gzip.decompress(textContentB64.encode()).decode()
            except Exception:
                textContent = textContentUndecoded  # Fallback to undecoded if error occurs
            
            if obj_id in objectIDs["misc"]["texts"]:
                texts.append(objectIDs["misc"]["texts"][obj_id] + f" (X: {xPos}, Y: {yPos})")
                texts.append(f"    Content: {textContent}")
        
        if texts:
            f.write("\nTexts in Level:\n\n")
            for text in texts:
                f.write(f"{text}\n")
                f.write("-" * 30 + "\n")
        else:
            f.write("No Texts found or all are unknown IDs.\n")

        #count coins
        coinCount = 0
        for obj in objectList:
            obj_id = str(obj.get("1"))
            if obj_id in objectIDs["coins"]:
                coinCount += 1

        if coinCount > 0:
            f.write(f"\nTotal Coins in Level: {coinCount}\n")
        else:
            f.write("No Coins found or all are unknown IDs.\n")
            
    print("Analysis saved successfully.")
    return