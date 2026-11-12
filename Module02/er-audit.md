# Task 1: Reconstruct the ER Model

## 1. Identify the entities and attributes

### Machine
- machine_name
- serial_no
- site
- installed

### Part
- part_no
- description
- unit_price

### MaintenanceJob
- job_id
- machine_name
- technician
- done_on
- parts_used

### Technician
- No separate technician table exists in the legacy database.
- Technician names are currently stored in the maint_job table.

## 2. Identify the relationships and cardinalities

1. Machine – MaintenanceJob (1:N)
   - One machine can have many maintenance jobs.
   - Each maintenance job belongs to one machine.

2. Technician – MaintenanceJob (1:N)
   - One technician can perform many maintenance jobs.
   - Each maintenance job is assigned to one technician.

3. MaintenanceJob – Part (M:N)
   - One maintenance job can use many parts.
   - One part can be used in many maintenance jobs.
   - This relationship requires a junction table, for example `MaintenanceJobPart`.



## Verify cardinalities with SQL

Machine → MaintenanceJob (1)

SQL query

SELECT machine_name, COUNT(*) AS job_count
FROM maint_job
GROUP BY machine_name;

╭──────────────┬───────────╮
│ machine_name │ job_count │
╞══════════════╪═══════════╡
│ cnc-01       │         2 │
│ cnc-02       │         1 │
│ cnc-05       │         1 │
╰──────────────┴───────────╯

## Interpretation

The results show that one machine can have multiple maintenance jobs. The record for cnc-05 also reveals a referential integrity problem because that machine does not exist in the machine table.

## Technician → MaintenanceJob (1)

SQL query

SELECT technician, COUNT(*) AS job_count
FROM maint_job
GROUP BY technician;

╭────────────┬───────────╮
│ technician │ job_count │
╞════════════╪═══════════╡
│ Beier      │         2 │
│ Klaas      │         1 │
│ Werther    │         1 │
╰────────────┴───────────╯

## Interpretation

The results support the intended one-to-many relationship: one technician can perform multiple maintenance jobs, while each maintenance job currently records one technician.

## Hidden relationship in the legacy schema

The legacy schema hides a many-to-many relationship between MaintenanceJob and Part.
Evidence:
Job 1 stores P-1001,P-1002 in a single parts_used field.
This means one maintenance job can use multiple parts.
The same part can also be used in different maintenance jobs.

## Task 2: Integrity defects

### Defect 1: Orphan maintenance jobs

**SQL query:**
```sql
SELECT m.job_id, m.machine_name
FROM maint_job m
LEFT JOIN machine x
    ON m.machine_name = x.machine_name
WHERE x.machine_name IS NULL;

╭────────┬──────────────╮
│ job_id │ machine_name │
╞════════╪══════════════╡
│      3 │ cnc-05       │
╰────────┴──────────────╯

## Understanding the results
- Maintenance job 3 refers to machine cnc-05.
- There is no machine named cnc-05 in the machine table.
- This is an orphan record: a record that refers to something that does not exist.

## Production impact:
An orphan maintenance job cannot be reliably attributed to a machine or its site, resulting in incomplete maintenance history and reports.

### Step 4: Repair idea

The proper model repair is to use a `machine_id` primary key in `machine` and a foreign key in `maint_job`. The existing `cnc-05` reference must also be corrected or its missing machine added, based on the real records.

## Defect 2: Duplicate natural keys in part

**SQL query:**

SELECT part_no, COUNT(*) AS copies
FROM part
GROUP BY part_no
HAVING COUNT(*) > 1;

╭─────────┬────────╮
│ part_no │ copies │
╞═════════╪════════╡
│ P-1003  │      2 │
╰─────────┴────────╯

Production impact:
Duplicate part numbers can cause incorrect stock counts, duplicate purchasing records, and unreliable inventory reports.

### Step 4: Repair idea

- Investigate why `P-1003` appears twice.
- Confirm whether both rows represent the same physical part.
- Remove the duplicate only after checking its references.
- Make `part_no` the primary key or add a `UNIQUE` constraint to prevent future duplicates.

### Defect 3: Unit price stored as text

**SQL query:**
SELECT part_no, unit_price
FROM part
WHERE unit_price < '15';

╭─────────┬────────────╮
│ part_no │ unit_price │
╞═════════╪════════════╡
│ P-1001  │ '12.50'    │
╰─────────┴────────────╯
Production impact: 
Text-based price comparisons can select the wrong parts, leading to incorrect invoices, discounts, and purchasing decisions.

### Repair idea

Change the `unit_price` column to a numeric type, such as `REAL` for this exercise, or preferably store money as an integer number of cents to avoid floating-point rounding issues.

### Defect 4: Installation dates that are not valid dates

**SQL query:**
SELECT machine_name, installed
FROM machine
WHERE installed NOT GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]';

╭──────────────┬───────────╮
│ machine_name │ installed │
╞══════════════╪═══════════╡
│ RANDOM-NAME  │ unknown   │
╰──────────────┴───────────╯
## Results Intepretation
The machine RANDOM-NAME has unknown in its installed column instead of a date in the expected YYYY-MM-DD format.

For example, a valid date would look like 2021-07-02.

Production impact:
Invalid installation dates can cause maintenance schedules, warranty calculations, and machine-age reports to produce incorrect results.

###  Repair idea
- Find the actual installation date for `RANDOM-NAME`.
- Replace `unknown` with the verified date.
- Store dates consistently and add validation so invalid values cannot be inserted.

### Defect 5: Many-to-many list fails to join correctly

**SQL query:**
SELECT j.job_id, p.description
FROM maint_job j
JOIN part p
    ON p.part_no = j.parts_used;

╭────────┬───────────────────╮
│ job_id │    description    │
╞════════╪═══════════════════╡
│      2 │ Coolant filter    │
│      2 │ Coolant filter    │
│      3 │ Ball bearing 6203 │
╰────────┴───────────────────╯
## Results Intepretation
Job 1 is missing because its parts_used value contains two part numbers separated by a comma. Job 2 appears twice because P-1003 is duplicated in the part table

### How should Defect 5 be repaired?

The proper solution is to create a junction table.This gives each part its own row and correctly represents the many-to-many relationship.


Task 3: Data contract — constraint decisions
## Constraints enforced by the application (Pydantic)
machine_id must be at least 1 (Field(ge=1)).
serial_no must contain at least 3 characters (Field(min_length=3)).
serial_no must start with SN- (field_validator).
installed and done_on must be valid dates (date type).

Why? These checks validate incoming application data before it is accepted or passed to the database. They provide clear validation errors to the application.

## Constraints enforced by the database (SQLAlchemy)
Primary keys uniquely identify machines, parts and maintenance jobs.
serial_no must be unique (UniqueConstraint).
Foreign keys ensure that maintenance jobs reference existing machines.
The job_part junction table uses a composite primary key and foreign keys to represent the many-to-many relationship.
unit_price uses NUMERIC(9, 2) rather than TEXT.
Required fields use nullable=False.

Why? Database constraints protect data integrity even when records are inserted or changed by different applications.