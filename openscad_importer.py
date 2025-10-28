from parser import Project, Element, Panel, DrillingGroup
from writer import write_s3d
import re

def import_from_echo(file_path: str) -> Project:
    """
    Imports a project from an OpenSCAD echo file.
    """
    project = Project()
    element = Element(
        name="Imported_Element",
        position={'X': '0', 'Y': '0', 'Z': '0'},
        dimensions={'Width': '0', 'Height': '0', 'Depth': '0'}
    )
    project.elements.append(element)

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('ECHO: "PANEL:'):
                match = re.search(r'ECHO: "PANEL:(.*)"|', line)
                if match:
                    panel_data = match.group(1).split(',')
                    name = panel_data[0]
                    w, h, d, x, y, z = [p.strip() for p in panel_data[1:]]
                    panel = Panel(
                        name=name,
                        position={'X': x, 'Y': y, 'Z': z},
                        dimensions={'Width': w, 'Height': h, 'Thickness': d},
                    )
                    element.panels.append(panel)

            elif line.startswith('ECHO: "DRILL:'):
                match = re.search(r'ECHO: "DRILL:(.*)"|', line)
                if match:
                    drill_data = match.group(1).split(',')
                    x, y, z, diameter, depth = [p.strip() for p in drill_data]
                    
                    if element.panels:
                        panel = element.panels[-1]
                        
                        rel_x = float(x) - float(panel.position['X'])
                        rel_y = float(y) - float(panel.position['Y'])
                        
                        drilling_group = DrillingGroup(data={
                            'RASNAM': 'drill',
                            'RASXPO': str(rel_x),
                            'RASYPO': str(rel_y),
                            'RASPLA': '1', # Hardcoded for now
                            'RASFI': diameter,
                            'RASDUB': depth,
                            'RASMODE': '0',
                            'RASBRR': '1',
                            'RASSVK': '0',
                            'RASANG': '0'
                        })
                        panel.drilling_groups.append(drilling_group)

    # Calculate element dimensions
    min_x, max_x = 0, 0
    min_y, max_y = 0, 0
    min_z, max_z = 0, 0

    for panel in element.panels:
        x = float(panel.position['X'])
        y = float(panel.position['Y'])
        z = float(panel.position['Z'])
        w = float(panel.dimensions['Width'])
        h = float(panel.dimensions['Height'])
        d = float(panel.dimensions['Thickness'])

        min_x = min(min_x, x)
        max_x = max(max_x, x + w)
        min_y = min(min_y, y)
        max_y = max(max_y, y + h)
        min_z = min(min_z, z)
        max_z = max(max_z, z + d)

    element.position['X'] = str(min_x)
    element.position['Y'] = str(min_y)
    element.position['Z'] = str(min_z)
    element.dimensions['Width'] = str(max_x - min_x)
    element.dimensions['Height'] = str(max_y - min_y)
    element.dimensions['Depth'] = str(max_z - min_z)

    return project

if __name__ == '__main__':
    project = import_from_echo('sample.echo')
    write_s3d(project, 'imported_from_openscad.s3d')
    print("Generated imported_from_openscad.s3d")