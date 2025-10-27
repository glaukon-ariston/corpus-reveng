Write a prompt for Gemini for the workflow and save it to @WORKFLOW.md
The workflow should include the following steps:
- Use git to keep track of the changes.
- Name the github project appropriately.
- Before every step check the available context and estimate the headroom needed to complete the task. Compress the context if needed.
- Before every new step create a new git branch that will hold all the changes for the step.
- Merge the changes from the previous step into the main branch.
- Update @GEMINI.md before starting a new step with the latest findings.
- Update @WORKFLOW.md whenever you realize something that is relevant to the project workflow.
- @WORKFLOW.md should contain generic intructions and @GEMINI.md should contain project specific instructions.