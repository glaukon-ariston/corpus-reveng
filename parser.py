import xml.etree.ElementTree as ET
import re
from dataclasses import dataclass, field
from typing import List, Dict
import pprint

@dataclass
class DrillingGroup:
    data: Dict[str, str]

@dataclass
class Panel:
    name: str
    position: Dict[str, str]
    dimensions: Dict[str, str]
    drilling_groups: List[DrillingGroup] = field(default_factory=list)

@dataclass
class Element:
    name: str
    position: Dict[str, str]
    dimensions: Dict[str, str]
    panels: List[Panel] = field(default_factory=list)

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

def parse_s3d(file_path: str) -> Project:
    """
    Parses an S3D file and returns a Project object.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    project = Project()

    for element_node in root.findall('ELEMENT'):
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
                    }
                )

                rupe_node = ad_node.find('RUPE')
                if rupe_node is not None:
                    for grupa_node in rupe_node.findall('GRUPA'):
                        data_string = grupa_node.get('DATA')
                        if data_string:
                            drilling_data = _parse_data_string(data_string)
                            drilling_group = DrillingGroup(data=drilling_data)
                            panel.drilling_groups.append(drilling_group)
                
                element.panels.append(panel)
        project.elements.append(element)

    return project

if __name__ == '__main__':
    project_data = parse_s3d('export/sobasav/Kuhinja_01.S3D')
    pprint.pprint(project_data)
