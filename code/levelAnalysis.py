import json
import os
import tempfile
from . import analyzeJsonLevel as analyze

# Mapping for Start Object Header Keys
START_OBJ_ATTR_MAP = {
    "kA1": "AudioTrack", "kA2": "Gmemode", "kA3": "Mini Mode", "kA4": "Speed",
    "kA5": "Obj-2 Blending", "kA6": "Background Texture ID", "kA7": "Ground Texture ID",
    "kA8": "Dual Mode", "kA9": "Level/Start Pos Object", "kA10": "2-Player Mode",
    "kA11": "Flip Gravity", "kA12": "Color3 Blending", "kA13": "Song Offset",
    "kA14": "Guidelines", "kA15": "Fade In", "kA16": "Fade Out", "kA17": "Ground Line",
    "kA18": "Font", "kA20": "Reverse Gameplay", "kA22": "Platformer Mode",
    "kA25": "Middleground Texture ID", "kA27": "Allow Multi-Rotation",
    "kA28": "Mirror Mode", "kA29": "Rotate Gameplay", "kA31": "Enable Player Squeeze",
    "kA32": "Fix Gravity Bug", "kA33": "Fix Negative Scale", "kA34": "Fix Robot Jump",
    "kA36": "Spawn Group", "kA37": "Dynamic Level Height", "kA38": "Sort Groups",
    "kA39": "Fix Radius Collision", "kA40": "Enable 2.2 Changes", "kA41": "Allow Static-Rotate",
    "kA42": "Reverse Sync", "kA43": "No Time Penalty", "kA45": "Decrease Boost Slide",
    "kS38": "Colors", "kS39": "Color Page"
}

# Mapping for Color Channel Data (used to parse kS38)
COLOR_ATTR_MAP = {
    1: "Red", 2: "Green", 3: "Blue",
    4: "Player Color", 5: "Blending", 6: "Colour Channel Index",
    7: "Opacity", 8: "Toggle Opacity", 9: "Inherited Colour Channel Index",
    10: "HSV", 11: "Target Red", 12: "Target Green", 13: "Target Blue",
    14: "Delta Time", 15: "Target Opacity", 16: "Duration", 17: "Copy Opacity"
}

def sanitize_string(s):
    """
    Removes non-printable characters from a string to ensure valid JSON.
    Keeps newlines, tabs, and standard text.
    """
    if not isinstance(s, str):
        return s
    # Allow printable characters and common whitespace, remove others (like null bytes)
    return "".join(c for c in s if c.isprintable() or c in ['\n', '\r', '\t'])

def analyzeLevelData(levelData: str, levelID):
    # 1. Split Header and Objects
    if ';' in levelData:
        header_part, objects_part = levelData.split(';', 1)
    else:
        header_part = levelData
        objects_part = ""

    # 2. Parse Header
    levelStartObj = extractLevelStartObject(header_part)

    # 3. Parse Objects
    levelObjectsArr = []
    if objects_part:
        raw_objects = objects_part.split(';')
        
        for obj_str in raw_objects:
            if not obj_str.strip():
                continue
                
            parts = obj_str.split(',')
            current_obj = {}
            
            # Iterate through parts in pairs
            for i in range(0, len(parts) - 1, 2):
                try:
                    key = parts[i]
                    value = parts[i+1]
                    # Sanitize values to prevent JSON serialization errors
                    current_obj[key] = sanitize_string(value)
                except IndexError:
                    continue
            
            levelObjectsArr.append(current_obj)

    # 4. Write to JSON safely using a temporary file
    data_to_write = {
        "Level Start Object": levelStartObj,
        "Level Objects": levelObjectsArr
    }

    if not os.path.exists("savedLevelsAsJson"):
        os.makedirs("savedLevelsAsJson")

    filename = f"{levelID}_levelAnalysis.json"
    filePath = os.path.join("savedLevelsAsJson", filename)
    
    # Use a temporary file to prevent partial/corrupt writes
    temp_path = filePath + ".tmp"
    
    try:
        # Write to temp file with UTF-8 encoding explicitly
        with open(temp_path, 'w', encoding='utf-8') as jsonFile:
            json.dump(data_to_write, jsonFile, indent=4, ensure_ascii=True)
        
        # If write was successful, replace the old file (if any) with the new one
        if os.path.exists(filePath):
            os.remove(filePath)
        os.rename(temp_path, filePath)
        
        print(f"Level analysis written to {filePath}")
        print(f"Parsed {len(levelObjectsArr)} objects.")
        
        # Call the analysis function
        analyze.analyzeJsonLevel(True, filePath)
        
    except Exception as e:
        print(f"Error writing level analysis to JSON: {e}")
        # Clean up temp file if something went wrong
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass

def extractLevelStartObject(levelString):
    startObjInfo = {}
    parts = levelString.split(',')
    
    for i in range(0, len(parts) - 1, 2):
        key = parts[i]
        value = parts[i+1] if i+1 < len(parts) else None
        
        if not value:
            continue

        if key in START_OBJ_ATTR_MAP:
            attr_name = START_OBJ_ATTR_MAP[key]
            
            # --- PARSE GUIDELINES (kA14) ---
            if key == "kA14": 
                raw_guidelines = value.split('|')
                guidelines_list = []
                for gl in raw_guidelines:
                    if '~' in gl:
                        ts, col_id = gl.split('~')[0], gl.split('~')[1]
                        try:
                            guidelines_list.append({
                                "timestamp": float(ts),
                                "color_id": int(col_id)
                            })
                        except ValueError:
                            continue
                startObjInfo[attr_name] = guidelines_list

            # --- PARSE COLOR CHANNELS (kS38) ---
            elif key == "kS38": 
                raw_channels = value.split('|')
                channels_list = []
                
                for chan_str in raw_channels:
                    if not chan_str: continue
                    chan_parts = chan_str.split('_')
                    chan_data = {}
                    r, g, b = None, None, None 
                    tr, tg, tb = None, None, None 

                    for k_idx in range(0, len(chan_parts) - 1, 2):
                        try:
                            k_id = int(chan_parts[k_idx])
                            v_val = chan_parts[k_idx+1]
                            
                            if k_id in COLOR_ATTR_MAP:
                                prop_name = COLOR_ATTR_MAP[k_id]
                                chan_data[prop_name] = v_val
                                
                                if k_id == 1: r = int(v_val)
                                if k_id == 2: g = int(v_val)
                                if k_id == 3: b = int(v_val)
                                if k_id == 11: tr = int(v_val)
                                if k_id == 12: tg = int(v_val)
                                if k_id == 13: tb = int(v_val)
                        
                        except (ValueError, IndexError):
                            continue
                    
                    if r is not None and g is not None and b is not None:
                        chan_data["Hex Color"] = f"#{r:02x}{g:02x}{b:02x}".upper()
                    
                    if tr is not None and tg is not None and tb is not None:
                        chan_data["Hex Color (Target)"] = f"#{tr:02x}{tg:02x}{tb:02x}".upper()

                    if chan_data:
                        channels_list.append(chan_data)
                
                startObjInfo[attr_name] = channels_list

            # --- HANDLE STANDARD FIELDS ---
            else:
                if key in ["kA1", "kA2", "kA4", "kA6", "kA7", "kA17", "kA18", "kA25", "kA36", "kS39"]:
                    try:
                        startObjInfo[attr_name] = int(value)
                    except ValueError:
                        startObjInfo[attr_name] = value
                elif key == "kA13":
                    try:
                        startObjInfo[attr_name] = float(value)
                    except ValueError:
                        startObjInfo[attr_name] = value
                else:
                    if value in ['0', '1']:
                        startObjInfo[attr_name] = bool(int(value))
                    else:
                        startObjInfo[attr_name] = value
                        
    return startObjInfo