feat: Update material parsing and documentation

This commit updates the material parsing logic and documentation based on the analysis of the `DANIRA.S3D` file.

**`parser.py`**
- Updated the `Panel` data class to use `mat_name`, `mat_uid`, and `mat_folder` attributes instead of `material` and `banding`.
- Modified the `_parse_element` function to extract `MATNAME`, `MATUID`, and `MATFOLDER` attributes from `<AD>` tags.

**`scripts/extract_materials.py`**
- Created a new script to extract panel and banding materials from an S3D file.
- The script extracts `MATNAME` from `<AD>` tags for panel materials and `MATN` from `<POTROSNI>` and `<DEFTRITEM>` tags for banding materials.
- Added a detailed description to the script.

**`GEMINI.md`**
- Updated the "Material and Banding" section to reflect the new understanding of material attributes.
- Added a new section "Material Extraction from DANIRA.S3D" with the extracted materials.

**`artifacts/conversation.md`**
- Created a new file to store the conversation history.
