# SQL for Analytics Engineers

Learn SQL the way Analytics Engineers actually use it.

Most SQL courses teach syntax. This course teaches you how to think.

I learned SQL on the job. I could write queries that worked, but nobody ever explained *why* experienced Analytics Engineers approached problems the way they did. Over time, I learned through code reviews, production issues, and solving real business problems.

This course is the guide I wish I had when I started.

Rather than memorizing SQL commands, you'll learn how to approach datasets, ask better questions, and build queries that are accurate, readable, and maintainable.

---

## Who This Course Is For

This course is designed for:

- Aspiring Analytics Engineers
- Data Analysts transitioning into Analytics Engineering
- SQL developers looking to strengthen analytical thinking
- Anyone who wants to move beyond memorizing syntax and start solving business problems with SQL

Whether you're brand new to SQL or have been writing queries for years, the focus is on building the habits of an Analytics Engineer.

---

# What You'll Learn

By the end of this course, you'll be able to:

- Understand the grain of a table before writing a query
- Filter data with confidence
- Aggregate data without introducing incorrect results
- Join tables while avoiding duplicate records
- Use window functions to answer analytical questions
- Know when to use CTEs versus subqueries
- Write SQL that is easy to read, review, and maintain
- Solve real-world business problems using SQL

---

# Course Structure

Each lesson follows the same format:

- 📖 Concept Overview
- 🧠 Think Like an Analytics Engineer
- 💻 Worked Examples
- ✍️ Practice Exercises
- 🚀 Challenge Problem

Solutions for every lesson are included in the `solutions/` folder.

---

# Lessons

| Lesson | Topic |
|---------|-------|
| 1 | Thinking in Tables |
| 2 | Filtering Data |
| 3 | Aggregations & GROUP BY |
| 4 | Joins |
| 5 | Window Functions |
| 6 | CTEs vs. Subqueries |
| 7 | Real Business Case Study |

---

# Repository Structure

```
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

- **data/** contains the datasets used throughout the course.
- **lessons/** contains the lesson content and exercises.
- **solutions/** contains completed solutions for each lesson.
- **course.duckdb** is the database file DuckDB creates.
- **duckdb.md** walks through installing DuckDB and setting up your environment.
- **setup.sql** loads the course datasets into DuckDB.


---

# Getting Started

1. Clone this repository.
2. Follow the instructions in **duckdb.md** to install DuckDB.
3. Run `setup.sql` to create the course tables.
4. Start with **Lesson 1 – Thinking in Tables**.

---

# Course Philosophy

Writing SQL isn't about getting the correct answer once.

It's about writing queries that someone else can understand six months from now.

Throughout this course, you'll practice writing SQL that is:

- ✅ Correct
- ✅ Readable
- ✅ Maintainable
- ✅ Easy to debug
- ✅ Ready for production

You'll also learn to think about the business question before writing a single line of SQL.

Because that's what Analytics Engineers do.

---

# Contributing

Found a typo or have an idea for improving a lesson?

Feel free to open an issue or submit a pull request.

---

Happy querying.

**Think like an Analytics Engineer.**