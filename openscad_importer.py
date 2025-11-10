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

    panels = []
    drills = []

    with open(file_path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if line.startswith('ECHO: "PANEL:'):
                match = re.search(r'ECHO: "PANEL:(.*)"', line)
                if match:
                    panel_data = match.group(1).split(',')
                    name = panel_data[0]
                    w, h, d, x, y, z = [p.strip() for p in panel_data[1:7]]
                    material = panel_data[7].strip() if len(panel_data) > 7 else ""
                    banding = [p.strip() for p in panel_data[8:12]] if len(panel_data) > 11 else ["", "", "", ""]

                    panel = Panel(
                        name=name,
                        position={'X': x, 'Y': y, 'Z': z},
                        dimensions={'Width': w, 'Height': h, 'Thickness': d},
                        mat_name=panel_data[7].strip() if len(panel_data) > 7 else "",
                        mat_uid=panel_data[8].strip() if len(panel_data) > 8 else "",
                        mat_folder=panel_data[9].strip() if len(panel_data) > 9 else ""
                    )
                    panels.append(panel)

            elif line.startswith('ECHO: "DRILL:'):
                match = re.search(r'ECHO: "DRILL:(.*)"', line)
                if match:
                    drill_data = match.group(1).split(',')
                    x, y, z, diameter, depth, nx, ny, nz = [p.strip() for p in drill_data]
                    drills.append({
                        'x': float(x), 'y': float(y), 'z': float(z),
                        'diameter': diameter, 'depth': depth,
                        'nx': float(nx), 'ny': float(ny), 'nz': float(nz)
                    })

    # Associate drills with panels
    for drill in drills:
        for panel in panels:
            px = float(panel.position['X'])
            py = float(panel.position['Y'])
            pz = float(panel.position['Z'])
            pw = float(panel.dimensions['Width'])
            ph = float(panel.dimensions['Height'])
            pd = float(panel.dimensions['Thickness'])

            # Check if the drill is inside the panel
            if (px <= drill['x'] <= px + pw) and \
               (py <= drill['y'] <= py + ph) and \
               (pz <= drill['z'] <= pz + pd):
                
                rel_x = drill['x'] - px
                rel_y = drill['y'] - py
                rel_z = drill['z'] - pz

                nx = drill['nx']
                ny = drill['ny']
                nz = drill['nz']

                abs_nx = abs(nx)
                abs_ny = abs(ny)
                abs_nz = abs(nz)

                raspla = '0' # Default
                if abs_nx > abs_ny and abs_nx > abs_nz:
                    if nx > 0: raspla = '6' # Right
                    else: raspla = '5' # Left
                elif abs_ny > abs_nx and abs_ny > abs_nz:
                    if ny > 0: raspla = '4' # Top
                    else: raspla = '3' # Bottom
                elif abs_nz > abs_nx and abs_nz > abs_ny:
                    if nz > 0: raspla = '2' # Back
                    else: raspla = '1' # Front
                
                if raspla == '1' or raspla == '2': # Front or Back
                    rasxpo = rel_x
                    rasypo = rel_y
                elif raspla == '3' or raspla == '4': # Bottom or Top
                    rasxpo = rel_x
                    rasypo = rel_z
                elif raspla == '5' or raspla == '6': # Left or Right
                    rasxpo = rel_y
                    rasypo = rel_z
                else:
                    rasxpo = rel_x
                    rasypo = rel_y

                drilling_group = DrillingGroup(data={
                    'RASNAM': 'drill',
                    'RASXPO': str(rasxpo),
                    'RASYPO': str(rasypo),
                    'RASPLA': raspla,
                    'RASFI': drill['diameter'],
                    'RASDUB': drill['depth'],
                    'RASMODE': '0',
                    'RASBRR': '1',
                    'RASSVK': '0',
                    'RASANG': '0'
                })
                panel.drilling_groups.append(drilling_group)
                break

    element.panels = panels
    
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
    project = import_from_echo('tmp/dummy.echo')
    write_s3d(project, 'imported_from_openscad2.s3d')
    print("Generated imported_from_openscad2.s3d")