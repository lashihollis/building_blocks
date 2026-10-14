# Financial File Tracker

A small Python data engineering learning project that determines which incoming financial transaction files should be processed, skipped, or flagged for investigation.

## Problem

A financial data pipeline may receive transaction files late, more than once, or while an earlier attempt is still running. Simply processing every file in an incoming folder can cause duplicate work and unsafe retries.

This project uses **file metadata**, **content checksums**, and **heartbeat timestamps** to make safer file-selection decisions before processing begins.

> **Scope:** This is a file-selection and testing project. It does not ingest transaction rows, update a database, schedule jobs, or process files itself.

## Project structure

```text
financial_pipeline/
├── file_tracker.py        # File-selection logic and helper functions
├── test_file_tracker.py   # Automated tests with pytest
└── README.md              # Project documentation
```

## How it works

```text
Incoming files + previous processing metadata
                    |
                    v
       Check previously successful
          content by checksum
                    |
             Already done? ---- Yes ---> Skip
                    |
                    No
                    v
       Check checksums selected
          during this run
                    |
           Already selected? -- Yes ---> Skip
                    |
                    No
                    v
         Look up filename status
                    |
          +---------+----------+
          |                    |
     New / FAILED          PROCESSING
          |                    |
          v                    v
    Ready to process     Check heartbeat age
                               |
                      +--------+--------+
                      |                 |
                 Missing/stale       Recent
                      |                 |
                      v                 v
               Investigate           Skip
```

The `get_files_to_process()` function returns a dictionary with two lists:

- `ready_to_process`: filenames eligible for a new attempt or retry.
- `needs_investigation`: filenames marked `PROCESSING` whose heartbeat is missing or older than the threshold.

Files already processed successfully, duplicate files selected in the current run, and files that appear actively processing are omitted from both lists.

## Business rules

| Scenario | Decision | Reason |
| --- | --- | --- |
| File has no metadata | Process | It has not been tracked previously |
| File has `SUCCESS` status / matching successful checksum | Skip | Content was already processed successfully |
| File has `FAILED` status | Retry | Previous attempt did not succeed |
| Two eligible files have the same checksum | Select one | Avoid selecting identical content twice in the same run |
| File has `PROCESSING` status and missing/stale heartbeat | Investigate | Worker may have stalled or crashed |
| File has `PROCESSING` status and recent heartbeat | Skip | Worker appears active |

The stale condition uses **heartbeat age > threshold** (not `>=`).

## Functions

### `is_duplicate_file(checksum, file_metadata)`

Checks whether a matching checksum has a previous `SUCCESS` record in persistent metadata.

### `is_file_stale(status, minutes_since_heartbeat, stale_threshold)`

Returns `True` only for `PROCESSING` files with a missing heartbeat or a heartbeat older than the configured threshold.

### `get_files_to_process(available_files, file_metadata, current_time, stale_threshold)`

Combines checksum checks, filename status lookup, and heartbeat evaluation to classify incoming files. It maintains an in-memory `selected_checksums` set for the duration of each function call.

## Example

```python
from datetime import datetime
from file_tracker import get_files_to_process

available_files = [
    {"filename": "transactions_0900.csv", "checksum": "aaa111"},
    {"filename": "transactions_0900_copy.csv", "checksum": "aaa111"},
    {"filename": "transactions_1000.csv", "checksum": "bbb222"},
]

file_metadata = [
    {
        "filename": "transactions_1000.csv",
        "checksum": "bbb222",
        "status": "SUCCESS",
        "last_heartbeat": None,
    }
]

result = get_files_to_process(
    available_files,
    file_metadata,
    current_time=datetime.fromisoformat("2026-10-13 12:00:00"),
    stale_threshold=15,
)

print(result)
# {
#     'ready_to_process': ['transactions_0900.csv'],
#     'needs_investigation': []
# }
```

The checksum strings above are illustrative placeholders. A real pipeline would compute hashes from file contents.

## Run the tests

Install Python 3 and pytest, then run these commands from the project directory:

```bash
python -m pip install pytest
python -m pytest -v
```

The seven automated tests cover:

1. New file selection.
2. Successful file skipping.
3. Failed file retry eligibility.
4. Duplicate content selected once.
5. Stale processing file flagged for investigation.
6. Active processing file skipped.
7. First eligible duplicate selected when the copy appears before a previously failed original.

## Data engineering concepts demonstrated

- **Metadata:** Store processing outcomes separately from incoming files.
- **Idempotency-related design:** Avoid reselecting content already processed successfully; selecting once is not the same as guaranteeing exactly-once execution.
- **Checksums:** Compare file content identity independently of filename.
- **Failure recovery:** Make failed files eligible for retry while treating potentially stalled work more cautiously.
- **Heartbeats:** Estimate whether an in-progress job is still active.
- **Observability:** Surface suspicious processing states for investigation.
- **Automated testing:** Verify pipeline decisions with repeatable assertions.

## Learning-version assumptions and limitations

- `file_metadata` is passed into the function; the project does not implement durable metadata storage.
- File processing, status updates, and retry execution are outside scope.
- The logic assumes a single selector. Multiple workers would need atomic claims or locking to prevent races.
- Input dictionaries are assumed to have the expected keys, valid statuses, and well-formed timestamps.
- Timestamps must be mutually compatible; production code should use timezone-aware timestamps and handle malformed/future heartbeat values.
- Selection order matters when multiple eligible filenames share a checksum: the first eligible file wins.
- The code does not verify file content or compute checksums itself.
- The seven tests cover the core learning scenarios, not every production edge case.

## Project takeaway

Reliable data pipelines require more than moving files. They need explicit decisions about **what is new, what has already succeeded, what can safely retry, and what needs human or automated investigation**. This project isolates those decisions in readable, testable Python code.
