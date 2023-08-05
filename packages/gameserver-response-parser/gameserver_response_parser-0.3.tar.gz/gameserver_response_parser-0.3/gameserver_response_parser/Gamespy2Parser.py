def parse_gamespy2(data, addr):

    server_dict = { "_parser": "gamespy2", "_port": addr[1], "_ip": addr[0]}

    header = data[:5]
    if header == b"\x00CORY":
        payload = data[5:].split(b'\x00')

        # build a dict from the response
        i = 0
        while i < len(payload) - 1:
            key = payload[i].decode()
            value = payload[i+1]
            server_dict[key] = value
            i+=2
        return server_dict
