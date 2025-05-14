def parse_hex(hex_code):
    \"\"\"Convert HEX to RGB tuple.\"\"\"
    hex_code = hex_code.lstrip("#")
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
