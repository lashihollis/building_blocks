"""Select incoming transaction files for processing or investigation."""

from datetime import datetime


def is_file_stale(status, minutes_since_heartbeat, stale_threshold):
    """Return whether a PROCESSING file has a missing or stale heartbeat."""
    return (
        status == "PROCESSING"
        and (
            minutes_since_heartbeat is None
            or minutes_since_heartbeat > stale_threshold
        )
    )


def is_duplicate_file(checksum, file_metadata):
    """Return whether identical contents have already processed successfully."""
    for record in file_metadata:
        if record["checksum"] == checksum and record["status"] == "SUCCESS":
            return True
    return False


def get_files_to_process(
    available_files, file_metadata, current_time, stale_threshold
):
    """Classify files for processing or investigation.

    This learning version assumes valid, consistently formatted metadata,
    timezone-compatible datetimes, and a single selection worker.
    """
    ready_to_process = []
    needs_investigation = []
    selected_checksums = set()

    for file in available_files:
        checksum = file["checksum"]

        if is_duplicate_file(checksum, file_metadata):
            continue

        if checksum in selected_checksums:
            continue

        status = None
        last_heartbeat = None
        minutes_since_heartbeat = None

        for record in file_metadata:
            if file["filename"] == record["filename"]:
                status = record["status"]
                last_heartbeat = record["last_heartbeat"]
                break

        if last_heartbeat is not None:
            last_heartbeat = datetime.fromisoformat(last_heartbeat)
            minutes_since_heartbeat = (
                current_time - last_heartbeat
            ).total_seconds() / 60

        if status is None or status == "FAILED":
            ready_to_process.append(file["filename"])
            selected_checksums.add(checksum)
        elif is_file_stale(status, minutes_since_heartbeat, stale_threshold):
            needs_investigation.append(file["filename"])

    return {
        "ready_to_process": ready_to_process,
        "needs_investigation": needs_investigation,
    }