# Reflection 2

## Take-away

Module 2 helped me understand why database design and data integrity are important when developing reliable applications. I learned how to identify entities, attributes, primary keys, foreign keys and relationships using ER diagrams.

I also learned about the different relationship types: one-to-one (1:1), one-to-many (1) and many-to-many (M). I understood that many-to-many relationships should be represented using a junction table rather than storing several values in one database column.

## What was good?

I particularly enjoyed working with the legacy maintenance database because it allowed me to identify real database problems using SQL queries. I learned how to reconstruct an ER model from existing database tables and detect invalid dates and unsuitable data types.

## What was difficult?

One of my main challenges was understanding how to reconstruct an ER diagram from an existing database that did not have proper primary keys and foreign keys.
I initially found it difficult to understand how a many-to-many relationship works and why a junction table is necessary.

## Exploration and show stoppers
I explored how database design problems can affect real applications. The legacy database exercise showed me that duplicate part numbers can lead to unreliable inventory records, while orphan maintenance jobs can make it difficult to identify which machine was serviced.


## Interaction with peers and instructors

The lecturer's instructions and examples helped me understand the expected structure of the exercises. I followed the provided Module 2 tasks and used the lecturer's code conventions when creating my data contract.I also learned the importance of checking the assignment requirements before adding extra features or changing anything.

## How did you verify AI suggestions?
I used AI as a learning assistant to explain database concepts, understand SQL queries. I checked the generated SQL against the lecturer's instructions, ran the Python script in my terminal and inspected the generated DDL to confirm that the four expected tables were created. However, I learned that AI-generated answers should not automatically be trusted.


## Help and extra work

During this module, I used additional explanations and practical examples to improve my understanding of ER modelling, data contracts from youtube videos and online searches.
