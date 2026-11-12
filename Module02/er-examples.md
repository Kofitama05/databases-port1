1. One-to-one (1:1): Machine and Nameplate
Entities and attributes
Machine: machine_id (PK), machine_name
Nameplate: serial_no (PK), manufacturer, machine_id (FK)

![alt text](<One-to-one (11) Machine and Nameplate.jpg>)


2. One-to-many (1:N): Machine and Sensor
Entities and attributes
Machine: machine_id (PK), machine_name
Sensor: sensor_id (PK), sensor_type, machine_id (FK)
![alt text](<One-to-many (1N) Machine and Sensor.jpg>)

3. Many-to-many (M:N): WorkOrder and Part
Entities and attributes
WorkOrder: order_id (PK), order_date
Part: part_id (PK), part_name
WorkOrderPart: order_id (PK, FK), part_id (PK, FK), quantity

![alt text](<Many-to-many (MN) WorkOrder and Part.jpg>)

4. Entity vs attribute vs relationship: MaintenanceJob
Entities and attributes
MaintenanceJob: job_id (PK), job_date, machine_id (FK), technician_id (FK)
Machine: machine_id (PK), machine_name
Technician: technician_id (PK), technician_name

![alt text](<Entity vs attribute vs relationship MaintenanceJob.jpg>)

## SQL proof of cardinality: Machine and Sensor 

## Create the tables

CREATE TABLE machine (
    machine_id INTEGER PRIMARY KEY,
    machine_name TEXT NOT NULL
);

CREATE TABLE sensor (
    sensor_id INTEGER PRIMARY KEY,
    sensor_type TEXT NOT NULL,
    machine_id INTEGER NOT NULL,
    FOREIGN KEY (machine_id) REFERENCES machine(machine_id)
);

## Insert sample data

INSERT INTO machine (machine_id, machine_name)
VALUES (101, 'CNC Machine 01');

INSERT INTO sensor (sensor_id, sensor_type, machine_id)
VALUES
    (1, 'Temperature', 101),
    (2, 'Vibration', 101);

## COUNT query

SELECT machine_id, COUNT(*) AS sensor_count
FROM sensor
GROUP BY machine_id;

## Results
╭────────────┬──────────────╮
│ machine_id │ sensor_count │
╞════════════╪══════════════╡
│        101 │            2 │
╰────────────┴──────────────╯