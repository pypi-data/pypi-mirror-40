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
        server_dict["_parser_subversion"] = "goldsource"
        pos = 5
        for key in ["address", "name", "map", "folder", "game"]:
            str_end = data.find(b"\x00", pos)
            server_dict[key] = bytes_to_str(data[pos:str_end])
            pos = str_end+1
        # 3 Bytes as numbers
        for key in ["players", "max. players", "protocol"]:
            server_dict[key] = bytes_to_int(data[pos:pos+1])
            pos+=1
        # 2 Bytes as chars
        for key in ["server type","environment"]:
            server_dict[key] = bytes_to_str(data[pos:pos+1])
            pos+=1
        # 2 Bytes as numbers
        for key in ["visibility", "mod"]:
            server_dict[key] = bytes_to_int(data[pos:pos+1])
            pos+=1

        # Check for special mod fields
        if server_dict["mod"] == 1:
            # 2 Strings
            for key in ["link", "download link"]:
                str_end = data.find(b"\x00", pos)
                server_dict[key] = bytes_to_str(data[pos:str_end])
                pos = str_end+1
            # skip NULL byte
            pos+=1
            # 2 longs
            for key in ["version", "size"]:
                server_dict[key] = bytes_to_int(data[pos:pos+4])
                pos+=4
            # 2 bytes as numbers
            for key in ["type", "dll"]:
                server_dict[key] = bytes_to_int(data[pos:pos+1])
                pos+=1
        # 2 Bytes as numbers
        for key in ["vac","bots"]:
            server_dict[key] = bytes_to_int(data[pos:pos+1])
            pos+=1

        return server_dict

    return
