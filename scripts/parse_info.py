
"""
This script parses the hexadecimal data from the INFO and SELBOX tags in S3D files.

It decodes the hexadecimal string into bytes and then interprets the data structure.
The script identifies a header and then reads the rest of the data in 4-byte chunks,
displaying the hexadecimal value and the ASCII representation of the first byte of each chunk.

This script is intended for reverse engineering the S3D file format.

Usage:
    python parse_info.py

The script uses a hardcoded hexadecimal string from a sample S3D file and writes the
parsed data to 'parsed_danira.txt'.
"""
import binascii
import os

def parse_selbox_data(data, output_file=None):
    """
    Parses the hexadecimal data from the SELBOX tags.
    """
    with open(output_file, 'w', encoding='utf-8') if output_file else open(os.devnull, 'w') as f:
        i = 0

        # Read header
        header_len = data[1]
        header = data[2:2+header_len].decode('latin-1')
        f.write(f"Header: {header}\n")
        i = 2 + header_len

        # Skip the next 6 bytes, which seem to be constant
        i += 6

        # Read the rest of the data in 4-byte chunks
        while i < len(data):
            chunk = data[i:i+4]
            if len(chunk) == 4:
                hex_val = chunk.hex()
                ascii_char = chr(chunk[0]) if 32 <= chunk[0] <= 126 else '.'
                f.write(f"  Chunk: {hex_val}, First byte: {ascii_char}\n")
            i += 4

if __name__ == '__main__':
    artifacts_dir = "artifacts"
    os.makedirs(artifacts_dir, exist_ok=True)
    hex_data = "070D5473656C656374696F6E426F780102000602555103650D0603707473000000000000000000000000000000000000000000660D0000670D0000680D0000690D00006A0D00006B0D00006C0D00006D0D00006E0D00006F0D0000700D0000710D0000720D0000730D0000740D0000750D0000760D0000770D0000780D0000790D00007A0D000000"
    data = binascii.unhexlify(hex_data)
    output_path = os.path.join(artifacts_dir, 'parsed_danira.txt')
    parse_selbox_data(data, output_file=output_path)
    print(f"Parsed data saved to {output_path}")
