import xml.etree.ElementTree as ET
import re

def parse_data_string(data_string):
    """
    Parses the DATA attribute string into a dictionary.
    """
    data = {}
    # Use regex to find all key=value pairs
    # The keys are alphanumeric, and the values are enclosed in double quotes
    # or are numeric.
    # This regex will find all occurrences of the pattern: "key=value"
    # where value can be a quoted string or a number.
    pattern = re.compile(r'([a-zA-Z0-9_]+)=([^,]+)')
    matches = pattern.findall(data_string)
    for key, value in matches:
        # Strip quotes from the value
        data[key] = value.strip('\"')
    return data

def parse_s3d(file_path):
    """
    Parses an S3D file and extracts information about furniture elements,
    panels, and drilling.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    for element in root.findall('ELEMENT'):
        print(f"Element: {element.get('ENAME')}")
        print(f"  Position: (X={element.get('EXPOX')}, Y={element.get('EYPOS')}, Z={element.get('EZPOS')})")
        print(f"  Dimensions: (Width={element.get('ESIRINA')}, Height={element.get('EVISINA')}, Depth={element.get('EDUBINA')})")

        daske = element.find('DASKE')
        if daske is not None:
            print("  Panels:")
            for ad in daske.findall('AD'):
                print(f"    - {ad.get('DNAME')}:")
                print(f"        Dimensions: (Width={ad.get('VISINA')}, Height={ad.get('DUBINA')}, Thickness={ad.get('DEBLJINA')})")

                rupe = ad.find('RUPE')
                if rupe is not None:
                    print("        Drilling:")
                    for grupa in rupe.findall('GRUPA'):
                        data_string = grupa.get('DATA')
                        if data_string:
                            drilling_data = parse_data_string(data_string)
                            print(f"          - Group: {drilling_data.get('RASNAM', 'N/A')}")
                            for key, value in drilling_data.items():
                                print(f"              {key}: {value}")

if __name__ == '__main__':
    parse_s3d('export/sobasav/Kuhinja_01.S3D')