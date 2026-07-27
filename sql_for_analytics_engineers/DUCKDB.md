# Using DuckDB for This Course

This course uses **DuckDB** as its local SQL database.

DuckDB is free, lightweight, and requires no separate database server. Everything for this course runs from a single database file on your computer.

---

# Repository Structure

Your repository should look like this:

```text
sql_for_analytics_engineers/
├── data/
│   ├── patients.csv
│   ├── providers.csv
│   ├── visits.csv
│   └── claims.csv
├── lessons/
├── solutions/
├── course.duckdb
├── README.md
├── DUCKDB.md
└── setup.sql
```

- **data/** contains the CSV files used throughout the course.
- **setup.sql** creates the database tables.
- **course.duckdb** is the database file DuckDB creates.

---

# Step 1: Install DuckDB

Visit the official DuckDB installation page:

https://duckdb.org/docs/installation/

### macOS (Homebrew)

```bash
brew install duckdb
```

Verify the installation:

```bash
duckdb --version
```

### Windows

Download the DuckDB CLI from the installation page above.

Open PowerShell and verify the installation:

```powershell
duckdb --version
```

If DuckDB is not on your PATH:

```powershell
.\duckdb.exe --version
```

---

# Step 2: Open the Course Folder

Open a terminal and navigate to the root of the repository.

Example:

```bash
cd path/to/sql-course
```

You should now be in the folder containing:

```text
data/
setup.sql
README.md
```

---

# Step 3: Create the Database

From the root of the repository, run:

```bash
duckdb course.duckdb
```

If the database does not exist, DuckDB will create it.

You should now see a prompt similar to:

```text
D
```

You are now inside DuckDB.

---

# Step 4: Load the Course Data

Inside DuckDB, execute:

```text
.read setup.sql
```

The setup script will:

- Create the tables
- Load the CSV files
- Verify that everything loaded successfully

You should see output similar to:

```text
┌────────────┐
│    name    │
├────────────┤
│ patients   │
│ providers  │
│ visits     │
│ claims     │
└────────────┘
```

Followed by the number of rows loaded into each table.

---

# Step 5: Verify the Data

List the tables:

```sql
SHOW TABLES;
```

Preview the patients table:

```sql
SELECT *
FROM patients
LIMIT 5;
```

Count the number of visits:

```sql
SELECT COUNT(*)
FROM visits;
```

---

# Helpful DuckDB Commands

Open an existing database:

```bash
duckdb course.duckdb
```

Run the setup script again:

```text
.read setup.sql
```

Exit DuckDB:

```text
.quit
```

Clear the screen:

```text
.clear
```

Show all tables:

```sql
SHOW TABLES;
```

Describe a table:

```sql
DESCRIBE patients;
```

Preview data:

```sql
SELECT *
FROM patients
LIMIT 10;
```

---