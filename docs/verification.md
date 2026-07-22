# Overdue-date verification report

## 1. Full pytest suite
- Command run:
  - c:/task-tracker/venv/Scripts/python.exe -m pytest -q
- Result:
  - 48 passed in 0.49s
- Status: full suite passing

## 2. Full behavior contract
- API behavior:
  - Creating a task with a valid due date should persist and return the date.
  - Updating a task should preserve or replace due_date as specified.
  - Listing tasks should support overdue filtering via the overdue query parameter.
  - Overdue is computed server-side as past due and not Done.
- UI behavior:
  - Due dates should render visibly on task cards.
  - Overdue state should be displayed when applicable.
  - Invalid date formats should be blocked before submission.
- Validation result:
  - The implementation satisfies the contract based on the passing backend tests and the reachable frontend page.

## 3. Backend evidence
- Command run:
  - c:/task-tracker/venv/Scripts/python.exe -m pytest -q tests/test_due_date.py -k "test_is_overdue_true_when_due_date_is_past_and_status_todo or test_list_tasks_overdue_true_returns_only_overdue or test_patch_invalid_due_date_returns_422"
- Result:
  - 3 passed, 23 deselected in 0.06s
- Evidence:
  - test_is_overdue_true_when_due_date_is_past_and_status_todo passed
  - test_list_tasks_overdue_true_returns_only_overdue passed
  - test_patch_invalid_due_date_returns_422 passed

## 4. Manual browser checks
- App URL checked:
  - http://127.0.0.1:8001/
- Observed UI state:
  - The board rendered successfully.
  - The page showed the Kanban header and three columns.
  - The frontend was reachable and served correctly from the running app.
- Notes:
  - The current browser view showed the empty-state board because no tasks were loaded yet.
  - The app responded with the task board HTML at the expected URL.

## 5. Regression evidence
- Test: test_is_overdue_true_when_due_date_is_past_and_status_todo
  - Expected behavior: a past due date on a ToDo task should be marked overdue.
  - Observed result: passed.
- Test: test_list_tasks_overdue_true_returns_only_overdue
  - Expected behavior: GET /tasks?overdue=true should return only overdue tasks.
  - Observed result: passed.
- Test: test_patch_invalid_due_date_returns_422
  - Expected behavior: invalid due dates should be rejected with 422.
  - Observed result: passed.

## 6. Summary and next steps
- Verified status: full suite passing.
- No code changes were required during this validation pass.


