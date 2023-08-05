def parse_gamespy(data, addr):
    data_split = data.split(b"\\")[1:]

    server_dict = {"_parser" : "gamespy", "_ip" : addr[0], "_port" : addr[1]}

    i = 0
    while i < len(data_split) - 1:
        key = data_split[i].decode()
        value = data_split[i+1]
        server_dict[key] = value
        i+=2

    return(server_dict)

