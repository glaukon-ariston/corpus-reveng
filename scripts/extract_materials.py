"""
This script parses an S3D XML file to extract unique material names used for panels and banding.

It identifies:
- Panel materials from the 'MATNAME' attribute within <AD> (panel) tags.
- Banding materials from the 'MATN' attribute within <POTROSNI> (consumables) and <DEFTRITEM> tags.

The script outputs two lists: one for unique panel materials and one for unique banding materials,
each sorted alphabetically.

Usage:
    python extract_materials.py <path_to_s3d_file>

Example:
    python extract_materials.py export/DANIRA.S3D
"""
import xml.etree.ElementTree as ET
import sys

def extract_materials(file_path):
    """
    Parses an S3D file and extracts unique panel and banding materials.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    panel_materials = set()
    banding_materials = set()
    
    # Extract panel materials from <AD> tags
    for ad_tag in root.findall('.//AD'):
        mat_name = ad_tag.get('MATNAME')
        if mat_name:
            panel_materials.add(mat_name)
            
    # Extract banding materials from <POTROSNI> and <DEFTRITEM> tags
    for potitem_tag in root.findall('.//POTITEM'):
        mat_n = potitem_tag.get('MATN')
        if mat_n:
            banding_materials.add(mat_n)
            
    for deftritem_tag in root.findall('.//DEFTRITEM'):
        mat_n = deftritem_tag.get('MATN')
        if mat_n:
            banding_materials.add(mat_n)
            
    return sorted(list(panel_materials)), sorted(list(banding_materials))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <file_path>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    try:
        panel_materials, banding_materials = extract_materials(file_path)
        
        print("Panel Materials:")
        for material in panel_materials:
            print(material)
            
        print("\nBanding Materials:")
        for material in banding_materials:
            print(material)

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        sys.exit(1)
    except ET.ParseError:
        print(f"Error: Could not parse XML from {file_path}")
        sys.exit(1)