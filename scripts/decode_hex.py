"""
This script decodes a hexadecimal string into a readable format.

It first converts the hexadecimal string to raw bytes and then attempts to decode
it using several common encodings (utf-8, latin-1, cp1252). This is useful for
reverse engineering the S3D file format, particularly for understanding the
content of tags like <INFO> and <SELBOX>.

Usage:
    python decode_hex.py

The script uses a hardcoded hexadecimal string from a sample S3D file and prints
the raw bytes and the decoded string to the console.
"""
import binascii

def decode_hex_string(hex_string):
    """
    Decodes a hexadecimal string into a readable format.
    """
    try:
        decoded_bytes = binascii.unhexlify(hex_string)
        print(f"Raw bytes: {decoded_bytes}")

        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                return decoded_bytes.decode(encoding)
            except UnicodeDecodeError:
                continue
        return "Could not decode with any of the attempted encodings."

    except binascii.Error as e:
        return f"Error decoding hex string: {e}"

if __name__ == '__main__':
    # Example usage with a hex string from the DANIRA.S3D file
    hex_data = "07105450726F6A6563744F706973446174610102000602555103640D0603646174116143E7E61390E54006036176610500000000000000000000060372616202000603627270120000000006046272726E120000000006046964776E120000000006036F706912000000000604706B757A0200060370696C020106047064696E11000000000090E54000"
    decoded_data = decode_hex_string(hex_data)
    print(f"Hex data: {hex_data}")
    print(f"Decoded data: {decoded_data}")
