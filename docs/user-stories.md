# User Stories: Due Date Support

## Feature 1: Due Dates +

### User Stories

| ID | Story | Acceptance Criteria | Notes / Assumptions |
| --- | --- | --- | --- |
| US-01 | As a team member, I want to add and validate a due date when creating or updating a task so that deadlines are captured accurately. | 1. Creating a task with a valid due date stores the date and returns it in the task payload. 2. Creating or updating a task with an invalid date format returns a validation error and does not save the task. 3. Updating an existing task with a blank or removed due date is accepted as no due date, without changing unrelated fields. | Due dates will use a simple date format such as YYYY-MM-DD. Validation occurs in the backend. |
| US-02 | As a team member, I want overdue tasks to be visually marked so that I can quickly identify work that needs attention. | 1. A task with a due date earlier than the current date is shown with an overdue indicator or pill. 2. Tasks with no due date or a future due date do not show the overdue indicator. 3. The overdue state is calculated consistently from the same backend date logic used by the API. | Overdue is computed in the backend and surfaced in the UI. |
| US-03 | As a team member, I want to set or change a due date from the task modal so that I can keep task details current without editing elsewhere. | 1. The task modal shows a due date field for both create and edit flows. 2. Saving a new due date updates the task and displays it on the task card. 3. If an invalid date is submitted, the task is not updated and the user sees a validation message. | This feature is limited to the existing shared task list experience. |
| US-04 | As a team member, I want to filter the task list to show only overdue tasks so that I can prioritize urgent work quickly. | 1. An overdue filter option returns only tasks whose due date is past due. 2. Clearing the filter restores the full task list. 3. The filter works for tasks already visible in the shared task list without requiring authentication or per-user lists. | This is a single-list filter for the shared board or list view. |

### Flagged AI Assumptions

| Story / Criterion | Assumption being made | Notes |
| --- | --- | --- |
| US-01 | Assumes valid due date support and invalid date format handling | Acceptance criteria 1 and 2 directly cover this behavior. |
| US-01, AC-2 | Assumes invalid date format is rejected | This is a clear failure-case requirement. |
| US-02 | Assumes overdue detection exists | Acceptance criteria 1 and 2 rely on overdue logic. |
| US-03 | Assumes due date can be updated | Acceptance criteria 1 and 2 assume create/edit flows support changing due dates. |
| US-04 | Assumes the filter returns only overdue tasks | Acceptance criterion 1 is the core behavior being assumed. |

### Corrected AI Assumptions

| ID | Story | Acceptance Criteria | Notes / Assumptions |
| --- | --- | --- | --- |
| US-01 | As a team member, I want to create and update tasks with a due date so that deadlines can be recorded and validated in the shared task list. | 1. A task can be created with a valid due date and the saved value is returned in the API response. 2. A task cannot be created or updated with an invalid date format, and the API returns a validation error. 3. A task can be updated to remove its due date, and the stored value becomes empty or null without changing other fields. | Due dates must be supported in both create and update flows. Validation is handled in the backend. |
| US-02 | As a team member, I want overdue tasks to be identified so that I can quickly focus on work that is past due. | 1. A task with a due date earlier than the current date is marked as overdue. 2. A task with no due date or a future due date is not marked as overdue. 3. Overdue status is determined by the same backend logic used by the API and UI. | Overdue detection is an explicit feature requirement. |
| US-03 | As a team member, I want to set or change a due date from the task modal so that task details stay current without leaving the existing workflow. | 1. The task modal includes a due date field in both create and edit modes. 2. Saving a new due date updates the task and shows the updated date on the task card. 3. If an invalid due date is submitted, the task is not saved and the user sees a validation message. | The update flow must support changing an existing due date. |
| US-04 | As a team member, I want to filter the task list to show only overdue tasks so that I can prioritize urgent work quickly. | 1. An overdue filter returns only tasks whose due date is past due. 2. Clearing the filter restores the full task list. 3. The overdue filter works within the existing shared task list and does not depend on authentication or per-user data. | Filtering by overdue status is a required feature for the shared list. |

## Feature 2: Tags/Labels

### User Stories

| ID | Story | Acceptance Criteria | Notes / Assumptions |
| --- | --- | --- | --- |
| TAG-01 | As a team member, I want to add tags to a task when creating or updating it so that related work can be grouped and found more easily. | 1. Creating a task with one or more valid tags stores those tags and returns them in the task payload. 2. Creating or updating a task with an empty tag value is rejected and the task is not saved. 3. Tags are trimmed so that surrounding whitespace does not create duplicate or invalid values. | Tags may be stored as a list or normalized comma-separated value. Validation occurs in the backend. |
| TAG-02 | As a team member, I want tags to appear as chips on task cards so that I can scan the shared list quickly. | 1. Each saved tag is displayed as a visible chip on the task card. 2. Tasks without tags do not show empty tag chips. 3. Tag chips remain visible after the task is updated with unrelated fields. | This is limited to the existing task card and shared list view. |
| TAG-03 | As a team member, I want to filter or search tasks by tag so that I can focus on work for a specific category. | 1. A tag filter or search input returns only tasks that contain the selected or entered tag. 2. Clearing the filter or search restores the full task list. 3. The filter works for tasks already visible in the shared task list without requiring authentication or per-user lists. | Tag filtering is a single-list feature for the shared board or list view. |
| TAG-04 | As a team member, I want to update task tags without losing other task details so that I can keep information current. | 1. Updating a task with a new set of tags changes only the tag values and preserves the other task fields. 2. An update request with valid tags succeeds and returns the updated task payload. 3. An update request with invalid tag values is rejected and the existing task remains unchanged. | This protects unrelated fields during tag updates. |

### Flagged AI Assumptions

| Story / Criterion | Assumption being made | Notes |
| --- | --- | --- |
| TAG-01 | Assumes tags can be created and stored with a task | This is a core feature assumption for create flow. |
| TAG-01, AC-2 | Assumes empty tag values are rejected | This is an explicit failure case for tag validation. |
| TAG-01, AC-3 | Assumes tags are trimmed before storage | This makes whitespace handling an expected rule. |
| TAG-02 | Assumes tags are displayed as visual chips on task cards | This is a UI-level assumption about how tags are presented. |
| TAG-03 | Assumes filtering or searching by tag is supported | This is a scope assumption for task-list interaction. |
| TAG-04 | Assumes tags can be updated without losing other task details | This assumes the update flow preserves unrelated fields. |

### Corrected AI Assumptions

| ID | Story | Acceptance Criteria | Notes / Assumptions |
| --- | --- | --- | --- |
| TAG-01 | As a team member, I want to create and update tasks with tags so that related work can be grouped and found more easily. | 1. A task can be created with one or more valid tags and the saved tags are returned in the API response. 2. A task cannot be created or updated with an empty tag value, and the API returns a validation error. 3. Tag values are trimmed before storage so surrounding whitespace does not create invalid duplicates. | Tags must be supported in both create and update flows. Validation is handled in the backend. |
| TAG-02 | As a team member, I want tags to appear as chips on task cards so that I can scan the shared list quickly. | 1. Each saved tag is displayed as a visible chip on the task card. 2. Tasks without tags do not show empty tag chips. 3. Tag chips remain visible after unrelated task fields are updated. | Tag display is a UI requirement for the existing shared task list. |
| TAG-03 | As a team member, I want to filter or search tasks by tag so that I can focus on work for a specific category. | 1. A tag filter or search input returns only tasks that contain the selected or entered tag. 2. Clearing the filter or search restores the full task list. 3. The filter works within the existing shared task list and does not depend on authentication or per-user data. | Tag filtering is a required feature for the shared list. |
| TAG-04 | As a team member, I want to update task tags without losing other task details so that I can keep information current. | 1. Updating a task with a new set of tags changes only the tag values and preserves the other task fields. 2. A valid tag update succeeds and returns the updated task payload. 3. An invalid tag update is rejected and the existing task remains unchanged. | The update flow must preserve unrelated task details. |
