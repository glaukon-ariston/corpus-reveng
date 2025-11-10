import xml.etree.ElementTree as ET
import re
from dataclasses import dataclass, field
from typing import List, Dict
import pprint

@dataclass
class Point:
    x: float
    y: float
    z: float

@dataclass
class Curve:
    points: List[Point] = field(default_factory=list)

@dataclass
class DrillingGroup:
    data: Dict[str, str]

@dataclass
class Panel:
    name: str
    position: Dict[str, str]
    dimensions: Dict[str, str]
    mat_name: str = ""
    mat_uid: str = ""
    mat_folder: str = ""
    drilling_groups: List[DrillingGroup] = field(default_factory=list)
    curves: List[Curve] = field(default_factory=list)

@dataclass
class Element:
    name: str
    position: Dict[str, str]
    dimensions: Dict[str, str]
    panels: List[Panel] = field(default_factory=list)
    elements: List['Element'] = field(default_factory=list)

@dataclass
class Project:
    elements: List[Element] = field(default_factory=list)

def _parse_data_string(data_string: str) -> Dict[str, str]:
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
        data[key] = value.strip('"')
    return data

def parse_krivulje_data(data_string: str) -> List[Point]:
    points = []
    
    # Split by comma, but not inside quotes
    parts = re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', data_string)

    kv_pairs = {}
    for part in parts:
        if '=' in part:
            key, value = part.split('=', 1)
            key = key.strip('" ')
            value = value.strip('" ')
            kv_pairs[key] = value

    point_data = {}
    i = 0
    while True:
        ptocka_key = f'PTOCKA'
        if ptocka_key in kv_pairs and kv_pairs[ptocka_key] == str(i):
            ptx_key = f'PTX'
            ptz_key = f'PTZ'
            
            if ptx_key in kv_pairs and ptz_key in kv_pairs:
                point_data['x'] = float(kv_pairs[ptx_key])
                point_data['z'] = float(kv_pairs[ptz_key])
                points.append(Point(x=point_data.get('x', 0.0), y=0.0, z=point_data.get('z', 0.0)))
                i += 1
                # Remove processed keys to avoid re-processing in the next iteration
                del kv_pairs[ptocka_key]
                del kv_pairs[ptx_key]
                del kv_pairs[ptz_key]
            else:
                break # PTX or PTZ not found for this PTOCKA
        else:
            break # PTOCKA not found or not sequential

    return points

def _parse_element(element_node: ET.Element) -> Element:
    element = Element(
        name=element_node.get('ENAME'),
        position={
            'X': element_node.get('EXPOX'),
            'Y': element_node.get('EYPOS'),
            'Z': element_node.get('EZPOS'),
        },
        dimensions={
            'Width': element_node.get('ESIRINA'),
            'Height': element_node.get('EVISINA'),
            'Depth': element_node.get('EDUBINA'),
        }
    )

    daske_node = element_node.find('DASKE')
    if daske_node is not None:
        for ad_node in daske_node.findall('AD'):
            panel = Panel(
                name=ad_node.get('DNAME'),
                position={
                    'X': ad_node.get('DXPOS'),
                    'Y': ad_node.get('DYPOS'),
                    'Z': ad_node.get('DZPOS'),
                },
                dimensions={
                    'Width': ad_node.get('VISINA'),
                    'Height': ad_node.get('DUBINA'),
                    'Thickness': ad_node.get('DEBLJINA'),
                },
                mat_name=ad_node.get('MATNAME', ''),
                mat_uid=ad_node.get('MATUID', ''),
                mat_folder=ad_node.get('MATFOLDER', '')
            )

            rupe_node = ad_node.find('RUPE')
            if rupe_node is not None:
                for grupa_node in rupe_node.findall('GRUPA'):
                    data_string = grupa_node.get('DATA')
                    if data_string:
                        drilling_data = _parse_data_string(data_string)
                        drilling_group = DrillingGroup(data=drilling_data)
                        panel.drilling_groups.append(drilling_group)
            
            krivulje_node = ad_node.find('KRIVULJE')
            if krivulje_node is not None:
                data_string = krivulje_node.get('DATA')
                if data_string:
                    points = parse_krivulje_data(data_string)
                    curve = Curve(points=points)
                    panel.curves.append(curve)

            element.panels.append(panel)

    elmlist_node = element_node.find('ELMLIST')
    if elmlist_node is not None:
        for child_element_node in elmlist_node.findall('ELM'):
            element.elements.append(_parse_element(child_element_node))

    return element

def parse_s3d(file_path: str) -> Project:
    """
    Parses an S3D file and returns a Project object.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    project = Project()

    for element_node in root.findall('./ELEMENT'):
        project.elements.append(_parse_element(element_node))

    return project

if __name__ == '__main__':
    project_data = parse_s3d('export/DANIRA.S3D')
    for element in project_data.elements:
        for panel in element.panels:
            if panel.curves:
                print(f"Panel: {panel.name}")
                pprint.pprint(panel.curves)
