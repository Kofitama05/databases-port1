# AI-generated SQL — Verification Notes

## Prompt used
Here is my SQLite table:
readings(ts TEXT, machine TEXT, temp_c REAL, vib_rms REAL, spindle_load REAL)

Write a SQL query that returns, for each machine, the average spindle load for readings taken overnight (after 18:00), ordered by average spindle load from highest to lowest.
Explain the query in simple terms because I am a beginner in SQL.

## Generated SQL
SELECT
    machine,
    AVG(spindle_load) AS avg_spindle_load
FROM readings
WHERE time(ts) > '18:00:00'
GROUP BY machine
ORDER BY avg_spindle_load DESC;

## Execution result
Record whether it ran successfully and include the actual output or error.

## Query plan
Run `EXPLAIN QUERY PLAN` before the query and paste the output.

Example:
```sql
EXPLAIN QUERY PLAN
SELECT machine, AVG(spindle_load) AS avg_load
FROM readings
WHERE ts > '2026-01-05 18:00:00'
GROUP BY machine
ORDER BY avg_load DESC;
```

## Verification and reflection
I ran the query in SQLite and checked the results. The average spindle load after 18:00 was highest for cnc-03, followed by cnc-01 and cnc-02.

I also used EXPLAIN QUERY PLAN. SQLite reported SCAN readings and temporary B-trees for grouping and sorting.

To verify the time filter, I compared the results with a query that used all readings without a WHERE clause. The results and machine ranking changed, confirming that the time filter affects the answer.

- What did the AI get right?
- What did it get wrong, if anything?
- How did I check the query's output and logic?
- Did the query plan show a table scan?

I learned to test AI-generated SQL by running it, inspecting its execution plan, and comparing its results with another query rather than trusting it without verification.
