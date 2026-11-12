Task 4: Model inheritance and prove it

Alternative A: Single table with a discriminator

All machines and their subtype-specific attributes are stored in one table. The machine_type column identifies the subtype.

CREATE TABLE machine (
    machine_id INTEGER PRIMARY KEY,
    serial_no TEXT NOT NULL UNIQUE,
    site TEXT NOT NULL,
    installed DATE NOT NULL,

    machine_type TEXT NOT NULL
        CHECK (machine_type IN ('CNC_MILL', 'INJECTION_MOLDER')),

    axes INTEGER,
    spindle_speed INTEGER,

    clamping_force REAL,
    injection_volume REAL,

    CHECK (
        (machine_type = 'CNC_MILL'
         AND axes IS NOT NULL
         AND spindle_speed IS NOT NULL
         AND clamping_force IS NULL
         AND injection_volume IS NULL)
        OR
        (machine_type = 'INJECTION_MOLDER'
         AND clamping_force IS NOT NULL
         AND injection_volume IS NOT NULL
         AND axes IS NULL
         AND spindle_speed IS NULL)
    )
);

How it works:
machine_type is the discriminator.
CNC mills use axes and spindle_speed.
Injection molders use clamping_force and injection_volume.
The CHECK constraints enforce the allowed types and disjointness: a machine cannot be both subtypes.
Some columns are NULL because they do not apply to every machine

Alternative B: Separate tables (joined-table inheritance)

The common machine attributes are stored in the parent table. Each subtype has its own table containing only its additional attributes.

CREATE TABLE machine (
    machine_id INTEGER PRIMARY KEY,
    serial_no TEXT NOT NULL UNIQUE,
    site TEXT NOT NULL,
    installed DATE NOT NULL
);

CREATE TABLE cnc_mill (
    machine_id INTEGER PRIMARY KEY,
    axes INTEGER NOT NULL,
    spindle_speed INTEGER NOT NULL,
    FOREIGN KEY (machine_id) REFERENCES machine(machine_id)
);

CREATE TABLE injection_molder (
    machine_id INTEGER PRIMARY KEY,
    clamping_force REAL NOT NULL,
    injection_volume REAL NOT NULL,
    FOREIGN KEY (machine_id) REFERENCES machine(machine_id)
);

How it works:
machine stores the shared attributes.
cnc_mill stores CNC-specific attributes.
injection_molder stores injection-molder-specific attributes.
Each child row must reference an existing machine.
A machine can have at most one row in each subtype table because machine_id is the primary key

