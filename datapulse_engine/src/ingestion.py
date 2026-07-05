# Day 2: Streaming and profiling logic
import csv
import sys
from pathlib import Path
from typing import Generator, Dict, Any

def stream_csv_file(file_path: Path) -> Generator[Dict[str, str], None, None]:
    """
    Streams a CSV file row by row as a dictionary using a generator.
    Keeps memory footprint constant regardless of file size.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Source data file not found: {file_path}")
        
    with open(file_path, mode="r", encoding="utf-8", newline="") as f:
        # Decision: Use DictReader so each row maps headers directly to string values
        reader = csv.DictReader(f)
        
        for row in reader:
            # The 'yield' keyword makes this function a generator. 
            # It pauses execution and hands control back to the loop, passing only ONE row.
            yield row

def profile_stream(file_path: Path) -> dict:
    """
    Iterates through the data stream to profile structural metadata 
    and verify stability before deep pipeline validation.
    """
    total_rows = 0
    malformed_rows = 0
    column_tracking = {}
    
    print(f"Beginning real-time profiling on stream: {file_path.name}")
    
    # Decision: Consume the generator row by row to gather metadata metrics
    for row in stream_csv_file(file_path):
        total_rows += 1
        
        # Check if the structure matches expected behavior
        row_len = len(row)
        column_tracking[row_len] = column_tracking.get(row_len, 0) + 1
        
        # Track rows that have missing or truncated column counts
        if None in row.values() or None in row.keys():
            malformed_rows += 1
            
    return {
        "total_ingested_rows": total_rows,
        "structural_anomalies": malformed_rows,
        "column_distribution": column_tracking
    }
