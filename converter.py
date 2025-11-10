"""
This script converts an OpenSCAD file to an S3D file.

It orchestrates the conversion process by:
1. Running OpenSCAD to generate an echo file containing panel and drill information.
2. Importing the data from the echo file to create a Project object.
3. Writing the Project object to an S3D file.

The script uses a temporary 'tmp' folder for intermediate files.

Usage:
    python converter.py <input_file.scad> <output_file.s3d>
"""
import argparse
import os
import subprocess
from openscad_importer import import_from_echo
from writer import write_s3d

def convert(input_file, output_file):
    """
    Converts an OpenSCAD file to an S3D file.
    """
    tmp_dir = "tmp"
    os.makedirs(tmp_dir, exist_ok=True)
    artifacts_dir = "artifacts"
    os.makedirs(artifacts_dir, exist_ok=True)

    file_ext = os.path.splitext(input_file)[1]

    if file_ext == '.scad':
        print(f"Running OpenSCAD on {input_file}...")
        echo_file = os.path.join(tmp_dir, os.path.basename(os.path.splitext(input_file)[0] + '.echo'))
        command = ['openscad', input_file, '-o', os.path.join(tmp_dir, 'dummy.stl')]
        with open(echo_file, 'w') as f:
            subprocess.run(command, stderr=f)
        print(f"Generated {echo_file}")
        input_file = echo_file
    
    print(f"Importing from {input_file}...")
    project = import_from_echo(input_file)

    output_path = os.path.join(artifacts_dir, output_file)
    print(f"Writing to {output_path}...")
    write_s3d(project, output_path)

    print("Conversion complete.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert OpenSCAD files to S3D format.')
    parser.add_argument('input', help='Input file (.scad or .echo)')
    parser.add_argument('output', help='Output file (.s3d)')
    args = parser.parse_args()

    convert(args.input, args.output)
