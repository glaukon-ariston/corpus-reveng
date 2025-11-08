feat: Implement recursive parsing for nested elements and curves

This commit introduces significant enhancements to the S3D parser, enabling it to handle more complex file structures, specifically nested elements and curved panels, as found in the `DANIRA.S3D` sample file.

### `parser.py`

- **Added `Point` and `Curve` data classes:** Introduced new data structures to represent 2D points and curves, allowing for the structured representation of panel shapes.
- **Enhanced `Panel` and `Element` classes:**
    - The `Panel` class now includes a `curves` field to store a list of `Curve` objects, enabling the representation of panels with custom shapes.
    - The `Element` class now features a recursive `elements` field, allowing for the parsing and representation of nested elements within the S3D file structure.
- **Implemented `parse_krivulje_data` function:** This new function is responsible for parsing the `DATA` attribute of `<KRIVULJE>` tags, extracting the point data for curved panels.
- **Introduced `_parse_element` recursive function:** A new recursive function, `_parse_element`, has been implemented to traverse the element tree, parsing nested elements and their associated panels, drillings, and curves.
- **Updated `parse_s3d` function:** The main `parse_s3d` function has been refactored to utilize the new `_parse_element` function, enabling the complete parsing of complex, nested S3D files.
- **Updated main execution block:** The main execution block has been updated to parse the `DANIRA.S3D` file and print the parsed curve data, serving as a test case for the new functionality.

### `prompts/latest.md`

- **Updated prompt:** The prompt has been updated to focus on the analysis of the `DANIRA.S3D` file, which was the catalyst for the new parsing features.

### Untracked Files

The following new files have been added to the project:

- `decode_hex.py`: A script to decode hexadecimal data.
- `parse_info.py`: A script to parse the `<INFO>` tag.
- `parse_krivulje.py`: A script to parse the `<KRIVULJE>` tag.
- `parse_selbox.py`: A script to parse the `<SELBOX>` tag.
- `parsed_danira.txt`: A text file containing the parsed output of `DANIRA.S3D`.
- `prompts/update.md`: The prompt file that initiated these changes.
