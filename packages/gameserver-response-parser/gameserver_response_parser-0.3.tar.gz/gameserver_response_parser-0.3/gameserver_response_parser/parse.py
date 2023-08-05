from .SRCDSParser import parse_srcds
from .Quake3Parser import parse_q3

def parse(data, addr):
    q3_header = b"\xFF\xFF\xFF\xFFstatusresponse"
    srcds_headers = [b"\xFF\xFF\xFF\xFF", b"\xFF\xFF\xFF\xFE"]

    if data.startswith(q3header):
        return parse_q3(data, addr)
    for header in srcds_headers:
        if data.startswith(header):
            if data[4] ==0x49 or data[4] == 0x6D:
                return parse_srcds(data, addr)
    return None

