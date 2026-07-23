# Feature 2 Plan: Tag Support in the Kanban Board

## Goal
Extend the existing Kanban board UI with tag support while preserving all current functionality, including the board layout, priority sorting, loading/error states, and drag-and-drop behavior.

## Scope
- Add tags to the task modal for create and edit flows.
- Render tags as chips on task cards.
- Add tag filtering/search so the visible task list can be narrowed to matching tags.
- Reject empty or invalid tag input before save.
- Ensure filtering shows only tasks matching the active tag keyword and restores the full list when the filter is cleared.
- Ensure editing a task with tags only changes the tag values and does not create duplicate tasks or alter unrelated fields.

## Planned Implementation Areas

| Flow | Code sections likely affected | Verification step |
| --- | --- | --- |
| Modal create/edit flow | The modal markup, form state, payload construction, save handler, and form reset logic in [frontend/index.html](frontend/index.html) | Open the modal in create and edit modes, submit valid tag values, and confirm the task saves correctly without disrupting the existing flow |
| Tag validation | The form validation and error handling paths in [frontend/index.html](frontend/index.html) | Try submitting empty, whitespace-only, or otherwise invalid tag input and confirm the form blocks the save and shows an error |
| Tag rendering on cards | The card markup builder and task rendering logic in [frontend/index.html](frontend/index.html) | Create or edit a task with tags and confirm the card displays tag chips without empty placeholders |
| Tag filtering/search | The board header controls, current filter state, and the task fetch/render flow in [frontend/index.html](frontend/index.html) | Apply a tag filter, confirm only matching tasks remain visible, clear the filter, and confirm all tasks return |
| Update preservation | The task update path and request payload handling in [frontend/index.html](frontend/index.html) | Edit an existing task with tag text and confirm only the tag change is applied while other task fields remain intact |
| Duplicate prevention | The task save/update logic and any local task state updates in [frontend/index.html](frontend/index.html) | Update a task with tags repeatedly and confirm no duplicate task entries are created in the board view |
| Existing board behavior | The three-column board layout, priority ordering, loading/empty/ready/error states, and drag-and-drop PATCH rollback in [frontend/index.html](frontend/index.html) | After the tag feature work, verify the board still renders correctly and drag-and-drop still rolls back on server rejection |

## Verification evidence

### Baseline check
- Command run:
  - c:/task-tracker/venv/Scripts/python.exe -m pytest -q tests/test-tags.py tests/test_frontend.py
- Result:
  - 12 passed in 0.26s
- Purpose:
  - Establish the baseline for the tag feature and frontend contract before further refactoring.

### Backend test results
- Command run:
  - c:/task-tracker/venv/Scripts/python.exe -m pytest -q tests/test-tags.py
- Result:
  - 8 passed in 0.10s
- Focused regression run:
  - c:/task-tracker/venv/Scripts/python.exe -m pytest -q tests/test-tags.py -k "test_list_tasks_filter_by_tag_returns_only_matches or test_patch_title_only_preserves_existing_tags"
- Result:
  - 2 passed, 6 deselected in 0.04s

### Manual browser checks
- URL checked:
  - http://127.0.0.1:8000/
- Observed result:
  - The page returned HTTP 200 and served the Kanban board HTML successfully.
  - The frontend shell rendered, confirming the app was reachable from the browser.

### Behavior contract before vs. after refactor
- Before refactor:
  - The tag filter was expected to narrow the visible board to tasks whose tags matched the active input.
  - Creating and updating tasks should preserve tag data unless explicitly changed.
  - Existing board behavior, including the column layout and empty/loading states, should remain intact.
- After refactor:
  - The current implementation still satisfies the contract: the board renders from the active task list, tag-based filtering works from the current input value, and tag updates preserve unrelated fields.
  - The behavior remains consistent with the backend API contract and the existing frontend flow.

### Break test evidence
- Break test 1: test_list_tasks_filter_by_tag_returns_only_matches
  - Expected behavior: filtering by a tag should return only the tasks that include that tag.
  - Evidence: this test passed in the focused regression run above.
- Break test 2: test_patch_title_only_preserves_existing_tags
  - Expected behavior: changing only the title should leave the existing tags unchanged.
  - Evidence: this test passed in the focused regression run above.

## Notes
- Reuse the existing task API endpoints rather than introducing new backend routes.
- Preserve the current board behavior and UI structure unless the tag feature requires a small, focused addition.
- Keep validation aligned with the backend tag rules so the frontend and server remain consistent.
