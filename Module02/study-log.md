## Basic ER Modelling Concepts

## Entity

An entity is an object, person, or thing about which we want to store information in a database. Examples include machines, technicians, sensors, and work orders. (https://deepanshutiw03.medium.com/understanding-entities-attributes-and-entity-relationships-f2c6e3992c02)

## Attribute

An attribute is a property that describes an entity. For example, a machine can have a machine ID, name, location, and installation date.(https://deepanshutiw03.medium.com/understanding-entities-attributes-and-entity-relationships-f2c6e3992c02)

## Relationship

A relationship describes how two or more entities are connected. For example, a machine can have several sensors, and a technician can perform maintenance on a machine.(https://deepanshutiw03.medium.com/understanding-entities-attributes-and-entity-relationships-f2c6e3992c02)

## Why ER Modelling Is Important

ER modelling helps us understand how data is organised and how different tables are connected before creating a database.

## Natural Key (NK)

Natural keys are attributes or combinations of attributes that already exist in the data and can uniquely pinpoint a record. (https://www.baeldung.com/sql/keys-natural-vs-surrogate)

## Surrogate Key (SK)

Surrogate keys, conversely, are artificial identifiers, typically auto-generated numbers or globally unique identifiers, created solely to uniquely identify records.(https://www.baeldung.com/sql/keys-natural-vs-surrogate)

##  Cardinality

### One-to-One (1:1)
One record in an entity is connected to exactly one record in another entity.
Example: One machine has one nameplate.

### One-to-Many (1:N)
One record in an entity can be connected to many records in another entity.
Example: One machine can have many sensors.

### Many-to-Many (M:N)
Many records in one entity can be connected to many records in another entity.
Example: Work orders can use several spare parts, and spare parts can be used in several work orders.

### What I learned
I learned how to identify one-to-one, one-to-many, and many-to-many relationships.


## Legacy database audit

I inspected the lecturer's legacy database using the `.schema` command.

I found the following problems:

1. The machine table has no primary key.
2. The part table allows duplicate part numbers.
3. The unit_price column stores prices as TEXT instead of a numeric type.
4. The maint_job table has no primary key.
5. The maintenance jobs use machine names instead of foreign keys.
6. Job 3 refers to cnc-05, which does not exist in the machine table.
7. The parts_used column contains multiple part numbers in one cell, violating 1NF.
8. Some values in parts_used are NULL.
9. Date columns are stored as TEXT without date validation.

This exercise helped me understand why database constraints, primary keys,
foreign keys and normalization are important.