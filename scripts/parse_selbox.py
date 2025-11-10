"""
This script parses the hexadecimal data from the SELBOX tags in S3D files.

It decodes the hexadecimal string, verifies the 'TselectionBox' header, and then
extracts a list of single-character identifiers from the data. The script assumes
that the identifiers are the first byte of each 4-byte chunk after the header.

This script is intended for reverse engineering the S3D file format.

Usage:
    python parse_selbox.py

The script uses a hardcoded hexadecimal string from a sample S3D file and prints
the extracted identifiers to the console.
"""
import binascii

def parse_selbox_data(hex_string):
    """
    Parses the hexadecimal data from the SELBOX tags.
    """
    data = binascii.unhexlify(hex_string)
    i = 0

    # Read header
    header_len = data[1]
    header = data[2:2+header_len].decode('latin-1')
    if header != 'TselectionBox':
        print("Error: Not a SELBOX block")
        return

    i = 2 + header_len

    # Skip the next 6 bytes, which seem to be constant
    i += 6

    # Read the rest of the data in 4-byte chunks
    identifiers = []
    while i < len(data):
        chunk = data[i:i+4]
        if len(chunk) == 4:
            identifier = chr(chunk[0])
            identifiers.append(identifier)
        i += 4

    return identifiers

if __name__ == '__main__':
    hex_data = "070D5473656C656374696F6E426F780102000602555103650D0603707473000000000000000000000000000000000000000000660D0000670D0000680D0000690D00006A0D00006B0D00006C0D00006D0D00006E0D00006F0D0000700D0000710D0000720D0000730D0000740D0000750D0000760D0000770D0000780D0000790D00007A0D000000"
    identifiers = parse_selbox_data(hex_data)
    if identifiers:
        print(f"Found {len(identifiers)} identifiers:")
        print(", ".join(filter(lambda x: x.isprintable(), identifiers)))
