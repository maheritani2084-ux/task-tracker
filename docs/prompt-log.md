## Feature 1:Due dates +
# prompt 1:generate backend for feature 1 --ACCEPTED and EDITED: the overdue date to ISO format in line 20: - Send due_date as an ISO date string (YYYY-MM-DD) in request bodies via date.isoformat().

You are a senior Python backend engineer. Add an optional due_date feature to my existing FastAPI app.
Context files:
@app/main.py
@app/models.py
@app/storage.py

Generate ONLY the model field additions and the modified GET /tasks route.

Exact specification:

MODELS (app/models.py):
- Add to TaskCreate: due_date: date | None = None
- Add to TaskUpdate: due_date: date | None = None
- Add to TaskResponse: due_date: date | None = None
- Add to TaskResponse: is_overdue: bool = False
- Add a field_validator on due_date in TaskCreate and TaskUpdate that rejects dates more than 365 days in the past -> raises ValueError -> HTTP 422 through Pydantic
- due_date must accept ISO 8601 date strings (YYYY-MM-DD) only; datetimes and malformed strings -> HTTP 422 through Pydantic

OVERDUE COMPUTATION:
- Computed in the BACKEND, not the UI. Rationale: single source of truth, consistent across clients, filterable server-side.
- Rule: is_overdue is True when due_date is not None AND due_date < date.today() AND status != TaskStatus.DONE
- Computed at response time, never stored in the _tasks dict

STORAGE (app/storage.py):
- Add a module-level helper: def compute_is_overdue(task: dict) -> bool
- add_task and update_task must persist due_date as-is; they must NOT compute or store is_overdue

ROUTE (app/main.py):
- Modify the existing GET /tasks route only
- Add optional query parameter: overdue: bool | None = Query(default=None)
- When overdue is None, return all tasks
- When overdue is True, return only tasks where compute_is_overdue is True
- When overdue is False, return only tasks where compute_is_overdue is False
- Existing filters on the route must continue to work and combine with overdue using AND logic

Imports to add at the top of app/models.py if missing:
from datetime import date
from pydantic import field_validator

Imports to add at the top of app/main.py if missing:
from fastapi import Query

Exact decorator and signature for the modified route:
@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(overdue: bool | None = Query(default=None)) -> list[TaskResponse]:
    ...

DO NOT:
- DO NOT store is_overdue in the _tasks dict.
- DO NOT compute overdue status in the frontend.
- DO NOT add a separate /tasks/overdue route.
- DO NOT modify POST, PATCH, GET by ID, or DELETE routes.
- DO NOT add manual date parsing; rely on Pydantic.
- DO NOT make due_date required.
- DO NOT use datetime.now() where date.today() is correct.

Output only the model field additions, the storage helper, the imports to add, and the modified route function in one code block.


## Feature 1: Due dates +
# Prompt 2: pytest prompt --ACCEPTED 
You are a senior Python developer writing pytest tests for a FastAPI app.
Context files:
@app/main.py
@app/models.py
@app/storage.py
@app/business_rules.py

Generate ONE file. Output only one code block, preceded by:
# FILE: tests/test_due_date.py

============================================================
FILE - tests/test_due_date.py
============================================================
Assume tests/conftest.py already exists and provides:
- _reset_storage autouse fixture
- client fixture
- created_task fixture

Use:
- pytest
- from datetime import date, timedelta

Generate these named tests:

CREATE with due_date:
- test_create_task_without_due_date_returns_201_and_null_due_date
- test_create_task_with_valid_due_date_returns_201_and_echoes_date
- test_create_task_with_malformed_due_date_returns_422
- test_create_task_with_datetime_string_due_date_returns_422
- test_create_task_with_due_date_older_than_365_days_returns_422
- test_create_task_with_due_date_exactly_365_days_ago_returns_201

UPDATE with due_date:
- test_patch_add_due_date_to_task_without_one_returns_200
- test_patch_change_existing_due_date_returns_200
- test_patch_clear_due_date_with_null_returns_200_and_null
- test_patch_title_only_does_not_change_due_date
- test_patch_invalid_due_date_returns_422

is_overdue COMPUTATION:
- test_is_overdue_false_when_due_date_is_null
- test_is_overdue_false_when_due_date_is_today
- test_is_overdue_false_when_due_date_is_future
- test_is_overdue_true_when_due_date_is_past_and_status_todo
- test_is_overdue_true_when_due_date_is_past_and_status_inprogress
- test_is_overdue_false_when_due_date_is_past_and_status_done
- test_is_overdue_not_persisted_in_storage_dict

OVERDUE QUERY FILTER on GET /tasks:
- test_list_tasks_without_overdue_param_returns_all
- test_list_tasks_overdue_true_returns_only_overdue
- test_list_tasks_overdue_false_returns_only_not_overdue
- test_list_tasks_overdue_true_excludes_done_tasks_with_past_due_date
- test_list_tasks_overdue_combined_with_status_filter_uses_and_logic
- test_list_tasks_overdue_combined_with_priority_filter_uses_and_logic
- test_list_tasks_overdue_true_empty_result_returns_200_and_empty_list
- test_list_tasks_overdue_invalid_value_returns_422

Hard constraints:
- Use TestClient only. Do not use AsyncClient.
- Do not mock storage. Use the real in-memory storage with the conftest reset fixture.
- Do not mock, freeze, or patch date.today(). Build all dates relative to date.today() using timedelta.
- Do not hardcode literal calendar dates such as "2026-01-01"; tests must not go stale.
- Send due_date as an ISO date string (YYYY-MM-DD) in request bodies via date.isoformat().
- For test_is_overdue_not_persisted_in_storage_dict, inspect storage._tasks directly and assert "is_overdue" is absent from the stored record.
- Do not skip or rename the listed tests.
- Do not re-test Module 2 behavior already covered in tests/test_tasks.py.
- Do not add tests unrelated to the due_date feature.
- Use the exact route paths and query parameter name from the app.

Output only the one file.


## Feature 1:Due dates +
## Prompt 3: fix Css ctyle for the due date label when overdue

You are a senior frontend engineer. Fix ONE styling detail in my existing task board.
Context files:
@index.html


Change the "Overdue" label on task cards from bare grey text to a red pill that is visually consistent with the existing priority pills (High / Medium / Low).

Exact specification:
- Reuse the exact same pill geometry as the priority pills: identical border-radius, padding, font-size, font-weight, and line-height. Read these values from the existing priority pill rule; do not invent new ones.
- Color scheme: light red / rose background with a dark red text color, following the same background-tint-plus-darker-text pattern the High priority pill already uses.
- The Overdue pill must remain visually distinct from the High priority pill. If High already uses red, shift the Overdue pill to a deeper red or add a thin border so the two are not confusable at a glance.
- Keep the label text "Overdue". Do not replace it with an icon only.
- Keep the due-date text ("Jan 30, 2026") red as it is now.
- Keep the pill in its current position on the card (right-aligned, same row as the due date).
- Preserve the existing aria-label or add aria-label="Overdue" so the state is announced to screen readers.

DO NOT:
- DO NOT change the priority pill styles.
- DO NOT change the card layout, spacing, or the position of the Edit button.
- DO NOT change when the pill renders; the is_overdue condition stays exactly as is.
- DO NOT introduce a new CSS framework, utility library, or inline style object if the project uses a stylesheet.
- DO NOT rename existing CSS classes.
- DO NOT rely on color alone; the word "Overdue" must stay visible.

Output only the changed CSS rule(s) and the changed JSX/HTML for the Overdue label, in one code block.

## Feature 1
## Weak prompt to fix the red pill for overdue of due date
Make the overdue label look better. It should be a red pill like the other pills on the card. Fix the styling so it matches. 

## this prompt was rejected because:
"Look better" is not a specification. It states a preference, not a target. The model must invent the acceptance criteria, so you can't evaluate the result against anything.

"Like the other pills" leaves the match unverified. Without pointing at the priority pill rule, the model produces a pill that is approximately similar — 6px radius against your 12px, 500 weight against your 600. Visually consistent was the entire point, and it's the thing most likely to come back wrong.

No context files means the model is guessing at your code. It has no idea whether you use a stylesheet, CSS modules, or Tailwind, so it picks one. If it guesses wrong you get a rewrite instead of an edit.

No scope fence invites collateral damage. This is the failure mode that costs the most time. Told only to "fix the styling," the model may restructure the card row, normalize the priority pills to match its new pill, or move the Edit button. You then debug regressions in code you never asked it to touch — the same class of problem as the NameError from route decorators landing in models.py.

It misses the one real design conflict. High priority is already a red pill. A prompt that says "make it a red pill" and stops produces two red pills on the same card that mean different things. The strong prompt anticipates this and requires disambiguation.

No accessibility constraint. Nothing stops the model from dropping the word "Overdue" for a red dot or icon, which breaks screen readers and colorblind users.

No output constraint. You get a full component rewrite plus prose explanation, and you have to diff it manually to find the three lines that actually changed.

## Feature 1
## Strong prompt for full behavior contract and full pytest validation
You are a senior QA and full-stack engineer validating the overdue-date feature for this task tracker.
Context files:
@app/main.py
@app/models.py
@app/storage.py
frontend/index.html
tests/test_due_date.py
tests/test_frontend.py

Perform a full validation pass for the feature and the application as a whole.

Required deliverables:
1. Full pytest suite
- Run the complete pytest suite and capture the exact command and output.
- Use pytest if available, especially:
  - c:/task-tracker/venv/Scripts/python.exe -m pytest -q
- Report whether the full suite is passing or failing.
- If failures exist, list the failing tests verbatim and do not claim success until they are resolved.

2. Full behavior contract
- Write a concise behavior contract that covers the expected behavior of the overdue-date feature.
- The contract must include:
  - API behavior for create, update, list, and filtering,
  - overdue calculation rules,
  - UI behavior for overdue display and invalid date handling.
- Validate the contract against the current implementation and note whether the implementation satisfies it.

3. Backend evidence
- Run the relevant pytest tests for backend behavior and include exact test names, commands, and observed results.
- Include evidence for both core overdue computation and overdue filtering.

4. Manual browser checks
- Open the app in a browser and verify the overdue-date behavior end to end.
- Check that:
  - a past-due task shows an overdue state,
  - a future or today task does not show overdue,
  - a Done task does not show overdue,
  - invalid date formats are blocked in the UI before submit,
  - due dates are rendered visibly on cards.
- Record the observed browser behavior clearly.

5. Regression and break-test evidence
- Select at least two representative tests and explain what would break if the overdue feature regressed.
- For each, include:
  - the test name,
  - the expected behavior,
  - the observed result during validation,
  - whether it passed or failed.

Hard constraints:
- Do not invent results. Every claim must be backed by fresh command output or observed browser behavior.
- Do not use vague statements like "looks fine" or "should work." Cite concrete evidence.
- If you change code, rerun the relevant tests and report the new results.
- Keep the output structured and concise.

Output format:
- Section 1: Full pytest suite
- Section 2: Full behavior contract
- Section 3: Backend evidence
- Section 4: Manual browser checks
- Section 5: Regression evidence
- Section 6: Summary and next steps

## Feature 2: tags/labels
### Prompt 1: backend tag support
- Prompt used:
  - "You are a senior Python backend engineer. Add tag support to my FastAPI task tracker. Context files: app/models.py, app/storage.py, app/main.py. Implement the backend so tasks can store tags, validate them, and support tag-based filtering on GET /tasks."
- What the prompt returned:
  - Added tag fields to the task models, validated tag input, persisted tags in storage, and enabled tag-based filtering on GET /tasks.
- What I did:
  - Accepted the implementation and kept the backend changes.

### Prompt 2: frontend tag UI
- Prompt used:
  - "You are a senior frontend engineer. Update the Kanban board so tasks can be tagged in the modal and rendered as chips on cards while preserving the existing board behavior."
- What the prompt returned:
  - Added tag input handling to the modal, rendered tag chips on cards, and preserved tag data during create/edit flows.
- What I did:
  - Accepted the main UI changes, then edited the result to better preserve the existing flow and avoid regressions.

### Prompt 3: tag filter bug fix
- Prompt used:
  - "Please fix the tag filter. It is not working properly in the frontend."
- What the prompt returned:
  - A first pass that touched the filter flow, but it did not fully capture the expected partial-match behavior for cases like 'work' matching 'work, urgent'.
- What I did:
  - Rejected the vague first pass as incomplete, then rewrote it into a stronger prompt and applied the corrected implementation.

### Weak prompt rewritten into a stronger prompt
- Weak prompt:
  - "Please fix the tag filter. It is not working properly in the frontend."
- Stronger prompt:
  - "You are a senior frontend engineer. Fix the tag filter in the Kanban board so the visible task list updates from the current tag input, supports partial matches, and includes tasks whose tags contain values like 'work' even when the stored tags are 'work, urgent'. Preserve the existing board layout and card rendering, and do not introduce new UI patterns."
- What the stronger prompt returned:
  - A targeted fix that aligned with the partial-match requirement and kept the rest of the board behavior intact.
- What I did:
  - Accepted the stronger version and kept the change.

### Prompt 4: verification evidence
- Prompt used:
  - "Generate verification evidence for Feature 2, including baseline checks, backend results, manual browser checks, behavior contract, and break-test evidence."
- What the prompt returned:
  - A structured verification summary with pytest output, browser check results, and notes on the behavior contract.
- What I did:
  - Accepted the summary and recorded it in the feature verification documentation.

