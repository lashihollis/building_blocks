import csv
import shutil
import pandas as pd
from pathlib import Path

# Paths
FILE = Path(__file__).parent / 'state_census_info.csv'
BACKUP = FILE.with_suffix('.csv.bak')
TEMP = FILE.with_suffix('.tmp.csv')

print(f'File: {FILE}')

# Make a backup
shutil.copy2(FILE, BACKUP)
print(f'Backup created: {BACKUP}')

# Read lines and remove repeated header lines (keep the first)
with FILE.open('r', encoding='utf-8') as f:
    lines = f.readlines()

if not lines:
    raise SystemExit('Empty file.')

# Normalize header line (strip trailing newline)
header_line = lines[0].rstrip('\n')
# Keep the first header and filter out identical header rows later in the file
new_lines = [lines[0]]
for ln in lines[1:]:
    if ln.rstrip('\n') == header_line:
        # skip repeated header
        continue
    new_lines.append(ln)

# Write temp cleaned CSV (without repeated header lines)
with TEMP.open('w', encoding='utf-8', newline='') as f:
    f.writelines(new_lines)

print(f'Wrote intermediate file without repeated header lines: {TEMP}')

# Load into pandas and drop duplicate rows based on the State column
# If the header starts with an empty column (index column), pandas will auto-detect it.

df = pd.read_csv(TEMP)
orig_rows = len(df)
print(f'Original parsed rows: {orig_rows}')

if 'State' not in df.columns:
    # Sometimes extra leading unnamed column exists; try to find 'State' column
    possible_state_cols = [col for col in df.columns if 'State' in str(col)]
    if possible_state_cols:
        state_col = possible_state_cols[0]
    else:
        # Fallback: assume second column contains state names
        state_col = df.columns[1]
else:
    state_col = 'State'

print(f'Using state column: {state_col}')

# Drop exact duplicates by 'State' (keep first), and also drop duplicates in entire row if any
before_drop = len(df)
# Drop exact duplicate rows (all columns equal)
df = df.drop_duplicates()
# Then drop duplicates by State only (if a same state exists with different columns, keep first)
df = df.drop_duplicates(subset=[state_col], keep='first')
after_drop = len(df)

print(f'Rows before drop: {before_drop}, after drop: {after_drop}, removed: {before_drop - after_drop}')

# Reset index (default 0..N-1) and write back to original CSV without writing an index column
# We'll keep the same header, but ensure index isn't written

df = df.reset_index(drop=True)

# Drop any lingering old index column (like 'Unnamed: 0') if present
if 'Unnamed: 0' in df.columns:
    df = df.drop(columns=['Unnamed: 0'])

# Create a clean index column and place it first
df.insert(0, 'index', df.index)

# Write out without pandas adding another index column
df.to_csv(FILE, index=False)

print(f'Cleaned CSV written back to: {FILE}')
# Remove temp file
TEMP.unlink()
print('Temporary files removed.')

# Summary
print('\nSummary:')
print(f'Backup: {BACKUP}')
print(f'Cleaned rows: {after_drop}')
print('Done.')
