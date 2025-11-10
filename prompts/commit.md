feat: Organize and document helper scripts

This commit organizes the helper scripts into the `scripts` folder and adds detailed descriptions to each of them. It also updates the project documentation to reflect these changes.

**`scripts/`**
- Moved `decode_hex.py`, `parse_info.py`, `parse_krivulje.py`, and `parse_selbox.py` into the `scripts` folder.
- Added detailed descriptions to the top of each of these scripts, explaining their purpose, usage, and providing an example.
- Fixed a duplicated `if __name__ == '__main__':` block in `scripts/parse_info.py`.

**`GEMINI.md`**
- Updated the "Artifacts" section to include the newly moved and documented scripts.

**`WORKFLOW.md`**
- Added a guideline to the "Documentation Guidelines" section to add a detailed description to the top of each script.

**`artifacts/conversation.md`**
- Updated with the latest conversation.
