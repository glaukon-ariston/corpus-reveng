# Project Workflow

This document outlines the development workflow for this project.

## Version Control

*   **Git Initialization:** The project will be managed using Git. A repository will be initialized at the beginning of the project.
*   **Branching:** For each distinct task or feature, a new branch will be created from the `main` branch. Branch names should be descriptive of the task (e.g., `feature/s3d-parser`, `fix/drilling-data-bug`).
*   **Commits:** Commits should be atomic and have clear, concise messages.
*   **Merging:** Once a task is complete and tested, the feature branch will be merged back into the `main` branch.

## Development Cycle

Each development cycle for a new task or feature will follow these steps:

1.  **Update `GEMINI.md`:** Before starting any new task, the `GEMINI.md` file will be updated with the latest findings, project-specific instructions, and goals for the upcoming task.
2.  **Create a New Branch:** A new branch will be created from the `main` branch to isolate the changes for the current task.
3.  **Context Review:** Before starting implementation, the available context will be reviewed to ensure there is enough headroom to complete the task. If necessary, the context will be compressed.
4.  **Implementation and Testing:** The task will be implemented, including any necessary tests.
5.  **Merge to Main:** After the task is completed and verified, the branch will be merged into the `main` branch.
6.  **Update `WORKFLOW.md`:** If any part of the workflow itself is improved or changed during the process, this `WORKFLOW.md` file will be updated accordingly.

## Documentation

*   `GEMINI.md`: This file will serve as the project's "memory" and will contain project-specific information, such as the current understanding of the S3D format, data structures, and the overall project plan.
*   `WORKFLOW.md`: This file contains the generic workflow instructions for the project. It should be updated whenever the development process is changed or refined.

## Documentation Guidelines

*   When updating `GEMINI.md`, do not delete information from it. Refine it by adding new information, such as learnings and artifacts, while keeping the original plan intact.
*   The `GEMINI.md` file should contain the original "Project Plan" and after that the "Project Execution", "Learnings", and "Artifacts" sections.

## OpenSCAD

To capture the `echo` output from an OpenSCAD script to a file, use the following PowerShell command:

```powershell
powershell -Command "openscad <input_file.scad> -o 'artifacts/dummy.png' --imgsize='1,1' 2>&1 | Out-File -FilePath 'artifacts/<output_file.echo>' -Encoding utf8"
```
