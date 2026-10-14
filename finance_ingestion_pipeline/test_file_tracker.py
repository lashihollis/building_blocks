"""Tests for the financial pipeline's file-selection rules."""

from datetime import datetime

from file_tracker import get_files_to_process


CURRENT_TIME = datetime.fromisoformat("2026-10-13 12:00:00")
STALE_THRESHOLD = 15


def file_record(filename, checksum):
    return {"filename": filename, "checksum": checksum}


def metadata_record(filename, checksum, status, last_heartbeat=None):
    return {
        "filename": filename,
        "checksum": checksum,
        "status": status,
        "last_heartbeat": last_heartbeat,
    }


def test_new_file_is_selected():
    result = get_files_to_process(
        [file_record("transactions_0700.csv", "new111")],
        [],
        CURRENT_TIME,
        STALE_THRESHOLD,
    )
    assert result["ready_to_process"] == ["transactions_0700.csv"]
    assert result["needs_investigation"] == []


def test_successful_file_is_skipped():
    result = get_files_to_process(
        [file_record("transactions_0800.csv", "aaa111")],
        [metadata_record("transactions_0800.csv", "aaa111", "SUCCESS")],
        CURRENT_TIME,
        STALE_THRESHOLD,
    )
    assert result["ready_to_process"] == []
    assert result["needs_investigation"] == []


def test_failed_file_is_retried():
    result = get_files_to_process(
        [file_record("transactions_0900.csv", "bbb222")],
        [metadata_record("transactions_0900.csv", "bbb222", "FAILED")],
        CURRENT_TIME,
        STALE_THRESHOLD,
    )
    assert result["ready_to_process"] == ["transactions_0900.csv"]
    assert result["needs_investigation"] == []


def test_duplicate_files_are_selected_once():
    result = get_files_to_process(
        [
            file_record("transactions_1000.csv", "ccc333"),
            file_record("transactions_1000_copy.csv", "ccc333"),
        ],
        [],
        CURRENT_TIME,
        STALE_THRESHOLD,
    )
    assert result["ready_to_process"] == ["transactions_1000.csv"]
    assert result["needs_investigation"] == []


def test_stale_processing_file_needs_investigation():
    result = get_files_to_process(
        [file_record("transactions_1100.csv", "ddd444")],
        [
            metadata_record(
                "transactions_1100.csv",
                "ddd444",
                "PROCESSING",
                "2026-10-13 11:30:00",
            )
        ],
        CURRENT_TIME,
        STALE_THRESHOLD,
    )
    assert result["ready_to_process"] == []
    assert result["needs_investigation"] == ["transactions_1100.csv"]


def test_active_processing_file_is_skipped():
    result = get_files_to_process(
        [file_record("transactions_1100.csv", "ddd444")],
        [
            metadata_record(
                "transactions_1100.csv",
                "ddd444",
                "PROCESSING",
                "2026-10-13 11:55:00",
            )
        ],
        CURRENT_TIME,
        STALE_THRESHOLD,
    )
    assert result["ready_to_process"] == []
    assert result["needs_investigation"] == []


def test_first_eligible_duplicate_is_selected():
    result = get_files_to_process(
        [
            file_record("transactions_1300_copy.csv", "eee555"),
            file_record("transactions_1300.csv", "eee555"),
        ],
        [metadata_record("transactions_1300.csv", "eee555", "FAILED")],
        CURRENT_TIME,
        STALE_THRESHOLD,
    )
    assert result["ready_to_process"] == ["transactions_1300_copy.csv"]
    assert result["needs_investigation"] == []
