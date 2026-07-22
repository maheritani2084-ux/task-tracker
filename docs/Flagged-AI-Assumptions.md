# Flagged AI Assumptions

# Feature 1: Due dates +

| Story / Criterion | Assumption being made | Notes |
| --- | --- | --- |
| US-01 | Assumes valid due date support and invalid date format handling | Acceptance criteria 1 and 2 directly cover this behavior. |
| US-01, AC-2 | Assumes invalid date format is rejected | This is a clear failure-case requirement. |
| US-02 | Assumes overdue detection exists | Acceptance criteria 1 and 2 rely on overdue logic. |
| US-03 | Assumes due date can be updated | Acceptance criteria 1 and 2 assume create/edit flows support changing due dates. |
| US-04 | Assumes the filter returns only overdue tasks | Acceptance criterion 1 is the core behavior being assumed. |

# Feature 2: Tags/Labels

| Story / Criterion | Assumption being made | Notes |
| --- | --- | --- |
| TAG-01 | Assumes tags can be created and stored with a task | This is a core feature assumption for create flow. |
| TAG-01, AC-2 | Assumes empty tag values are rejected | This is an explicit failure case for tag validation. |
| TAG-01, AC-3 | Assumes tags are trimmed before storage | This makes whitespace handling an expected rule. |
| TAG-02 | Assumes tags are displayed as visual chips on task cards | This is a UI-level assumption about how tags are presented. |
| TAG-03 | Assumes filtering or searching by tag is supported | This is a scope assumption for task-list interaction. |
| TAG-04 | Assumes tags can be updated without losing other task details | This assumes the update flow preserves unrelated fields. |
