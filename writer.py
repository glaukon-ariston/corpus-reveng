from parser import Project, Element, Panel, DrillingGroup

def _format_data_string(data: dict) -> str:
    """
    Formats a dictionary into a DATA attribute string.
    """
    return ','.join([key + '="' + value + '"' for key, value in data.items()])

def write_s3d(project: Project, file_path: str):
    """
    Writes a Project object to an S3D file.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" ?>\n')
        f.write('<PROJECTFILE>\n')
        for element_data in project.elements:
            f.write(f'  <ELEMENT ENAME="{element_data.name}" EXPOX="{element_data.position["X"]}" EYPOS="{element_data.position["Y"]}" EZPOS="{element_data.position["Z"]}" ESIRINA="{element_data.dimensions["Width"]}" EVISINA="{element_data.dimensions["Height"]}" EDUBINA="{element_data.dimensions["Depth"]}">\n')
            f.write('    <DASKE>\n')
            for panel_data in element_data.panels:
                f.write(f'      <AD DNAME="{panel_data.name}" DXPOS="{panel_data.position["X"]}" DYPOS="{panel_data.position["Y"]}" DZPOS="{panel_data.position["Z"]}" VISINA="{panel_data.dimensions["Width"]}" DUBINA="{panel_data.dimensions["Height"]}" DEBLJINA="{panel_data.dimensions["Thickness"]}">\n')
                if panel_data.drilling_groups:
                    f.write('        <RUPE>\n')
                    for drilling_group_data in panel_data.drilling_groups:
                        data_string = _format_data_string(drilling_group_data.data)
                        f.write(f'          <GRUPA DATA="{data_string}"/>\n')
                    f.write('        </RUPE>\n')
                f.write('      </AD>\n')
            f.write('    </DASKE>\n')
            f.write('  </ELEMENT>\n')
        f.write('</PROJECTFILE>\n')

if __name__ == '__main__':
    # Create a sample project
    project = Project(elements=[
        Element(
            name='Test_Element',
            position={'X': '0', 'Y': '0', 'Z': '0'},
            dimensions={'Width': '1000', 'Height': '800', 'Depth': '600'},
            panels=[
                Panel(
                    name='Test_Panel',
                    position={'X': '0', 'Y': '0', 'Z': '0'},
                    dimensions={'Width': '800', 'Height': '600', 'Thickness': '18'},
                    drilling_groups=[
                        DrillingGroup(data={
                            'RASNAM': 'test_raster',
                            'RASXPO': '100',
                            'RASYPO': '200',
                            'RASPLA': '1',
                            'RASFI': '5',
                            'RASDUB': '10',
                            'RASMODE': '1',
                            'RASBRR': '5',
                            'RASSVK': '32',
                            'RASANG': '0'
                        })
                    ]
                )
            ]
        )
    ])

    write_s3d(project, 'test_output.s3d')
    print("Generated test_output.s3d")