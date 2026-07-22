# Corrected AI Assumptions

# Feature 1: Due dates +

The stories below make the due-date assumptions explicit so the team can implement and test them directly.

| ID | Story | Acceptance Criteria | Notes / Assumptions |
| --- | --- | --- | --- |
| US-01 | As a team member, I want to create and update tasks with a due date so that deadlines can be recorded and validated in the shared task list. | 1. A task can be created with a valid due date and the saved value is returned in the API response. 2. A task cannot be created or updated with an invalid date format, and the API returns a validation error. 3. A task can be updated to remove its due date, and the stored value becomes empty or null without changing other fields. | Due dates must be supported in both create and update flows. Validation is handled in the backend. |
| US-02 | As a team member, I want overdue tasks to be identified so that I can quickly focus on work that is past due. | 1. A task with a due date earlier than the current date is marked as overdue. 2. A task with no due date or a future due date is not marked as overdue. 3. Overdue status is determined by the same backend logic used by the API and UI. | Overdue detection is an explicit feature requirement. |
| US-03 | As a team member, I want to set or change a due date from the task modal so that task details stay current without leaving the existing workflow. | 1. The task modal includes a due date field in both create and edit modes. 2. Saving a new due date updates the task and shows the updated date on the task card. 3. If an invalid due date is submitted, the task is not saved and the user sees a validation message. | The update flow must support changing an existing due date. |
| US-04 | As a team member, I want to filter the task list to show only overdue tasks so that I can prioritize urgent work quickly. | 1. An overdue filter returns only tasks whose due date is past due. 2. Clearing the filter restores the full task list. 3. The overdue filter works within the existing shared task list and does not depend on authentication or per-user data. | Filtering by overdue status is a required feature for the shared list. |

# Feature 2: Tags/Labels

The stories below make the tags assumptions explicit so the team can implement and test them directly.

| ID | Story | Acceptance Criteria | Notes / Assumptions |
| --- | --- | --- | --- |
| TAG-01 | As a team member, I want to create and update tasks with tags so that related work can be grouped and found more easily. | 1. A task can be created with one or more valid tags and the saved tags are returned in the API response. 2. A task cannot be created or updated with an empty tag value, and the API returns a validation error. 3. Tag values are trimmed before storage so surrounding whitespace does not create invalid duplicates. | Tags must be supported in both create and update flows. Validation is handled in the backend. |
| TAG-02 | As a team member, I want tags to appear as chips on task cards so that I can scan the shared list quickly. | 1. Each saved tag is displayed as a visible chip on the task card. 2. Tasks without tags do not show empty tag chips. 3. Tag chips remain visible after unrelated task fields are updated. | Tag display is a UI requirement for the existing shared task list. |
| TAG-03 | As a team member, I want to filter or search tasks by tag so that I can focus on work for a specific category. | 1. A tag filter or search input returns only tasks that contain the selected or entered tag. 2. Clearing the filter or search restores the full task list. 3. The filter works within the existing shared task list and does not depend on authentication or per-user data. | Tag filtering is a required feature for the shared list. |
| TAG-04 | As a team member, I want to update task tags without losing other task details so that I can keep information current. | 1. Updating a task with a new set of tags changes only the tag values and preserves the other task fields. 2. A valid tag update succeeds and returns the updated task payload. 3. An invalid tag update is rejected and the existing task remains unchanged. | The update flow must preserve unrelated task details. |
