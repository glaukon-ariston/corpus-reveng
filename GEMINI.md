# Project: Reverse Engineering Corpus S3D Format

@WORKFLOW.md

## Goal

The primary goal of this project is to reverse engineer the `.S3D` file format used by the Corpus application. The ultimate objective is to create a tool that can convert 3D models from OpenSCAD into the `.S3D` format, with a special focus on accurately representing drilling information for manufacturing purposes.

This will enable users to design furniture in OpenSCAD and generate files that can be directly used by cutting and drilling services that rely on the Corpus software.

## Initial Findings from Documentation

A review of the provided PDF documentation (`Osnovne upute 3.1.pdf`) has revealed several key concepts and technical details about the Corpus application and its data:

*   **Core Concepts:** The documentation outlines a hierarchical structure: `Projekt` (Project) -> `Element` (Element/Furniture) -> `Daska` (Panel). Panels are the fundamental building blocks.
*   **Panel Properties:** Panels have defined dimensions, position, and orientation. They can also have `Rubne trake` (edge bands) and `Krivulje` (curves) for custom shapes.
*   **Drilling Information:** `Potrošni materijal` (consumables), which includes hardware like screws and hinges, is linked to drilling operations. This confirms that drilling data is a key part of the file format.
*   **CNC and Data Export:** The software can export data for CNC machines. It also uses several external data files, which may be in a readable format:
    *   `cjeneposifri.dat`: A text file for pricing information.
    *   `ExcelTemp.xls`: An Excel file for data export.
    *   `Corpus.ini`: A configuration file.
    *   `varvalues.dat`: A file for variables.
*   **Coordinate System:** The documentation specifies a 3D coordinate system (X: left-right, Y: up-down, Z: front-back), which will be essential for correctly placing geometry.

## Project Plan

The project will be executed in the following phases:

### Phase 1: S3D File Format Analysis

1.  **Initial Inspection:** Analyze the raw content of a few small `.S3D` files from the `export` directory to determine if they are binary or text-based, and to get a feel for their structure.
2.  **Online Research:** Conduct a thorough web search for any existing documentation, discussions, or open-source projects related to the `.S3D` file format. Search terms will include "Corpus S3D file format", "S3D file specification", and ".s3d reverse engineering".
3.  **Comparative Analysis:** If no external documentation is found, perform a comparative analysis of the provided `.S3D` files. By comparing files with minor differences (e.g., `Kuhinja_01.S3D` vs. `Kuhinja_02.S3D`), we can isolate and identify the data structures that correspond to specific features like panel dimensions, positions, and drilling.

### Phase 2: Parser Development (Proof of Concept)

1.  **Tool Selection:** Based on the file format analysis, select the appropriate tools for parsing. Python, with libraries such as `struct` for binary data, is a strong candidate.
2.  **Initial Parser:** Develop a simple script to parse a single, relatively simple `.S3D` file.
3.  **Goal:** The initial goal for the parser will be to successfully extract basic information, such as the dimensions and names of the panels within the project.
4.  **Refactoring:** The parser was refactored to return a structured Python object (`Project`) instead of printing to the console. This makes the data more usable for future processing.

### Phase 2a: S3D Writer Development

A writer module (`writer.py`) has been developed to serialize the `Project` object back into the S3D XML format. This allows for the creation of new S3D files from scratch or the modification of existing ones.

### Phase 3: OpenSCAD Integration

1.  **Data Export from OpenSCAD:** Investigate the best method for exporting the required geometry and drilling information from an OpenSCAD model. This will likely involve creating a custom export script that generates an intermediate data file (e.g., in JSON or CSV format).
2.  **Intermediate Format Definition:** Define a clear and structured intermediate data format that will serve as the bridge between OpenSCAD and the `.S3D` converter.

### Phase 4: S3D Converter Implementation

1.  **Converter Scaffolding:** Build the main application that reads the intermediate data format.
2.  **S3D Generation:** Implement the logic to translate the data from the intermediate format into the binary structure of the `.S3D` file format, as determined in Phase 1 and 2.
3.  **Focus on Drilling:** Pay special attention to correctly encoding the drilling information, as this is a critical requirement for the project.

### Phase 5: Testing and Validation

1.  **Output Verification:** The primary method of testing will be to see if the generated `.S3D` files can be opened in the Corpus application or accepted by a cutting service.
2.  **Test Suite:** Create a collection of diverse OpenSCAD models to serve as a test suite, covering various scenarios and edge cases.
3.  **Iterative Refinement:** Continuously test and refine the converter to ensure the generated files are robust and accurate.

## Project Execution

### Phase 1: S3D File Format Analysis

This phase is complete. The `.S3D` file format is XML-based.

### Phase 2: Parser and Writer Development

This phase is complete. The `parser.py` and `writer.py` modules provide the core functionality for reading and writing `.S3D` files.

### Phase 3: OpenSCAD Integration

This phase is complete. The `openscad_importer.py` and the `converter.py` scripts provide a working pipeline for converting OpenSCAD files to the S3D format.

## Learnings

*   The `.S3D` file format is XML-based, which simplifies parsing.
*   The `echo` command in OpenSCAD can be used to export data in a custom format.
*   The `stderr` stream must be redirected to capture the `echo` output from OpenSCAD.
*   The output from OpenSCAD may contain a byte order mark (BOM), which needs to be handled when parsing the file.

## Artifacts

*   `parser.py`: A Python script to parse `.S3D` files into a structured `Project` object.
*   `writer.py`: A Python script to write a `Project` object to an `.S3D` file.
*   `openscad_importer.py`: A Python script to import data from an OpenSCAD `echo` file and create a `Project` object.
*   `converter.py`: A command-line tool to convert OpenSCAD files to the S3D format.
*   `sample.scad`, `sample.echo`: A simple OpenSCAD file and its corresponding echo output.
*   `sample2.scad`, `sample2.echo`: A more complex OpenSCAD file with drills on multiple faces, and its corresponding echo output.
*   `imported_from_openscad.s3d`, `imported_from_openscad2.s3d`, `sample2.s3d`: Sample `.S3D` files generated by the converter.

## Initial S3D File Analysis

Initial analysis of the `Kuhinja_01.S3D` file has revealed that the `.S3D` format is XML-based, not binary. This is a significant finding as it simplifies the parsing process considerably.

The XML structure is hierarchical, with the following key tags:

*   `<PROJECTFILE>`: The root element of the document.
*   `<ELEMENT>`: Represents a single piece of furniture.
*   `<DASKE>`: Contains the panels for a furniture element.
*   `<AD>`: Represents a single panel, with attributes for dimensions (`VISINA`, `DUBINA`, `DEBLJINA`), name (`DNAME`), and other properties.
*   `<RUPE>`: Contains drilling information for a panel.
*   `<GRUPA>`: Appears to define a group of holes, with drilling parameters stored in a `DATA` attribute.

The presence of the `<RUPE>` and `<GRUPA>` tags confirms that drilling information is stored directly in the file, and the data format within the `DATA` attribute appears to be a custom, delimited format.

## Detailed S3D File Analysis

A more detailed analysis of the `DANIRA.S3D` file has revealed several new tags and attributes that were not present in the initial analysis. These new findings are crucial for a more complete understanding of the S3D format.

*   **`<INFO>` and `<SELBOX>` tags:** These tags contain what appears to be hexadecimal encoded data. The purpose of this data is currently unknown and requires further investigation.
*   **`<ELMLIST>` and nested `<ELM>` tags:** The `DANIRA.S3D` file shows a nested structure of `<ELM>` tags within an `<ELMLIST>`. This suggests a hierarchical relationship between elements, which is not fully captured in the current `parser.py`.
*   **`<POTROSNI>` tag:** This tag, which translates to "consumables," is present and contains `<POTITEM>` tags. This confirms the "Initial Findings from Documentation" section in `GEMINI.md`.
*   **`<KRIVULJE>` tag:** This tag, for "curves," is used extensively. The `DATA` attribute for this tag is also a complex, comma-delimited format, similar to the drilling data. This is a significant area for further investigation, as it's likely used to define custom panel shapes.
*   **`<SPOJ>` and `<ELINKS>` tags:** These tags, meaning "joint" and "e-links" respectively, suggest a mechanism for defining relationships and connections between elements. The `<SPOJ>` tag contains `<M1>` and `<M2>` tags with `MSVA`, `MSFO`, `MSRA`, `MSPO`, and `MSMA` attributes, which seem to define the connection parameters.
*   **Formulas in attributes:** Many attributes, especially those related to position and dimensions (e.g., `XF`, `YF`, `ZF`, `HF`, `SF`, `DF`), contain formulas and references to other elements (e.g., `Š-Desna.Š`, `Visina-Gornja.Visina`). This is a powerful feature of the S3D format that allows for parametric design. The current parser and data model do not seem to handle this.

## Drilling Data Format

The drilling information is stored in the `DATA` attribute of the `<GRUPA>` tag within the `<RUPE>` section. The `DATA` attribute is a string of key-value pairs, separated by commas. The values are either numeric or strings enclosed in double quotes. The following are some of the key-value pairs that have been identified:

*   `RASXPO`, `RASYPO`: X and Y position of the raster of holes.
*   `RASPLA`: The face of the panel where the holes are drilled. (e.g. 1 for front, 2 for back, etc.)
*   `RASNAM`: The name of the raster.
*   `RASFI`: The diameter of the holes (from the symbol `fi`).
*   `RASDUB`: The depth of the holes.
*   `RASFXP`, `RASFYP`: These seem to be the same as `RASXPO` and `RASYPO`.
*   `RASCRE`: A boolean flag, always 1 in the analyzed file.
*   `RASMODE`: The mode of the raster. (e.g. 1 for a line of holes, 0 for a group, 3 for a saw cut).
*   `RASPRO`: Unknown.
*   `RASBRR`: The number of holes in the raster.
*   `RASSVK`: The distance between holes in the raster.
*   `RASANG`: The angle of the raster.

For saw cuts (`RASMODE=3`), the following additional keys are used:

*   `RASSTARTX`, `RASSTARTY`: The start coordinates of the cut.
*   `RASENX`, `RASENY`: The end coordinates of the cut.
*   `RASSIR`: The width of the cut.

For groups of holes (`RASMODE=0`), the following additional keys are used:

*   `RASRUFI`: The diameter of the holes in the group.
*   `RASRUDU`: The depth of the holes in the group.
*   `RASRUNX`, `RASRUNY`: The relative X and Y coordinates of each hole in the group.

## SELBOX Data Format

The `SELBOX` data appears to be a list of 4-byte identifiers. The first byte of each identifier seems to be an ASCII character, and the rest of the bytes are null. The data starts with a header that contains the string "TselectionBox".

## Next Steps

The current implementation provides a solid foundation for the project. The following are potential next steps for improving the converter:

*   **Refine Drill-to-Panel Association:** The current logic for associating drill holes with panels can be improved. A more robust solution would be to use the drill's normal vector to determine the correct face and then project the drill's coordinates onto that face.
*   **Support for More Complex Drilling Patterns:** The current implementation only supports single drill holes (`RASMODE=0`). The S3D format also supports line drills (`RASMODE=1`) and saw cuts (`RASMODE=3`).
*   **User Interface:** A more user-friendly interface (e.g., a graphical user interface) could be developed to make the converter easier to use.
*   **Error Handling and Validation:** Add more robust error handling and validation to the entire pipeline.
*   **Create an advanced parser for SELBOX data:** Create a more advanced parser for the `SELBOX` data to extract the list of identifiers and their meaning.
*   **Investigate INFO data:** Continue the investigation of the `INFO` data to understand its structure and meaning.
