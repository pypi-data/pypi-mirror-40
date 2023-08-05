def bytes_to_int(data):
    return int.from_bytes(data, byteorder='little')

def bytes_to_str(data):
    return data.decode('utf-8', 'ignore')

def parse_srcds(data, addr):
    server_dict = {"_ip": addr[0], "_port" : addr[1], "_parser" : "SRCDS"}

    header = data[4] #Header
    server_dict["header"] = header
    # new srcds format
    if header == 0x49: # modern srcds query
        server_dict["_parser_subversion"] = "srcds"
        #server_dict["protocol"] = bytes_to_int(data[1])
        server_dict["protocol"] = data[5]

        pos = 6

        # 4 String fields
        for key in ["name", "map", "folder", "game"]:
            str_end = data.find(b"\x00", pos)
            server_dict[key] = bytes_to_str(data[pos:str_end])
            pos = str_end+1

        # Steam Application ID (ID)
        server_dict["id"] = bytes_to_int(data[pos:pos+2])
        pos+=2

        # 3 Bytes interpreted as numbers
        for key in ["players", "max. players", "bots"]:
            server_dict[key] = bytes_to_int(data[pos:pos+1])
            pos+=1

        # 2 Bytes interpreted as strings
        for key in ["server type", "environment"]: #The game Rag Doll Kung Fu always returns 0 for server type
            server_dict[key] = bytes_to_str(data[pos:pos+1])
            pos+=1

        # 2 Bytes interpreted as numbers
        for key in ["visibility", "vac"]:
            server_dict[key] = bytes_to_int(data[pos:pos+1])
            pos+=1

        # special handling for The Ship packet format
        if server_dict["id"] == 2400: # The Ship AppID
            for key in ["mode", "witnesses", "duration"]:
                server_dict[key] = bytes_to_int(data[pos:pos+1])
                pos+=1

        # Version
        str_end = data.find(b"\x00", pos)
        server_dict["version"] = bytes_to_str(data[pos:str_end])
        pos = str_end+1

        # Extra Data Flag (EDF)
        if len(data) < pos:
            server_dict["edf"] = bytes_to_int(data[pos:pos+1])
            pos+=1

            # Handling of the EDF
            edf = server_dict["edf"]
            # port
            if edf & 0x80 != 0:
                server_dict["port"] = bytes_to_int(data[pos:pos+2])
                pos+=2
            # steamid of the server
            if edf & 0x10 != 0:
                server_dict["steamid"] = bytes_to_int(data[pos:pos+8])
                pos+=8
            # SourceTV data, since port and name are already in use the fields are called sourcetv_port and sourcetv_name
            if edf & 0x40 != 0:
                server_dict["sourcetv_port"] = bytes_to_int(data[pos:pos+2])
                pos+=2
                str_end = data.find(b"\x00", pos)
                server_dict["sourcetv_name"] = bytes_to_str(data[pos:str_end])
                pos = str_end+1
            # keywords
            if edf & 0x20 != 0:
                str_end = data.find(b"\x00", pos)
                server_dict["keywords"] = bytes_to_str(data[pos:str_end])
                pos = str_end+1
            # 64bit gameID, more accurate version of the AppID if the AppID did not fit into the 16bits
            if edf & 0x01 != 0:
                server_dict["gameid"] = byte_to_int(data[pos:pos+8])
                pos+=8

        return server_dict

    # old goldsource format
    if header == 0x6D:
        server_dict["protocol_subversion"] = "goldsource"
        payload = data[1:]
        address_end = payload.find(b"\x00")
        name_end                    = payload.find(b"\x00", address_end+1)
        mapname_end                 = payload.find(b"\x00",name_end+1)
        folder_end                  = payload.find(b"\x00",mapname_end+1)
        game_end                    = payload.find(b"\x00",folder_end+1)
        server_dict["server_name"]  = payload[0:name_end].decode('utf-8', 'ignore')  # Name
        server_dict["map"]          = payload[name_end+1:mapname_end].decode('utf-8', 'ignore') # Map
        server_dict["game"]         = payload[mapname_end + 1: folder_end].decode('utf-8', 'ignore') # Folder
        server_dict["game_type"]     = payload[folder_end + 1: game_end].decode('utf-8', 'ignore') # Game
        server_dict["players"]      = int.from_bytes(payload[game_end+1:game_end+2],byteorder='little') # Players
        server_dict["max_players"]  = int.from_bytes(payload[game_end+2:game_end+3], byteorder='little') # Max. Players
        server_dict["protocol"]    = int.from_bytes(payload[game_end+3:game_end+4],byteorder='little') # Bots
        server_type = payload[game_end+4:game_end+5].decode("utf-8", "ignore") # Server Type
        server_dict["server_type"]  = "dedicated"
        if server_type == "L":
            server_dict["server_type"]  = "non-dedicated"
        elif server_type == "P":
            server_dict["server_type"]  = "proxy" # SourceTV relay
        environment               = payload[game_end+5:game_end+6] # Environment
        server_dict["environment"] = "Windows" if environment == "W" else "Linux"
        password_protected = int.from_bytes(payload[game_end+6:game_end+7],byteorder='little') # Visibility
        server_dict["password_protected"] = password_protected != 0
        mod = int.from_bytes(payload[game_end+7:game_end+8],byteorder='little') # is this server modded
        server_dict["mod"] = (mod != 0)
        mod_end = game_end + 8
        #special options if mod is true
        if mod != 0:
            # now 2 strings, 1 byte, 2 longs, 2 bytes
            mod_start = game_end+8
            modwebsite_end = payload.find(b"\x00", mod_start)
            moddownload_end = payload.find(b"\x00", modwebsite_end)
            server["mod_website"] = payload[mod_start:modwebsite_end]
            server["mod_download"] = payload[modwebsite_end:moddownload_end]
            server_dict["mod_version"]= int.from_bytes(
                    payload[moddownload_end+1:moddownload_end+5],byteorder='little') #mod version
            server_dict["mod_size"]= int.from_bytes(
                    payload[moddownload_end+5:moddownload_end+9],byteorder='little') #mod download size
            server_dict["mod_type"]= int.from_bytes(
                    payload[moddownload_end+9:moddownload_end+10],byteorder='little') #mod type (multiplayer or singleplayer)
            server_dict["mod_dll"]= int.from_bytes(
                    payload[moddownload_end+9:moddownload_end+10],byteorder='little') #mod dll (does the mod use a dll)
            mod_end = moddownload_end+10
        # VAC is skipped
        server_dict["bot_count"] = int.from_bytes(payload[mod_end:mod_end+1], byteorder='little')

        return server_dict


    return

