## The Six Clauses and the Plan
Relational algebra is a procedural query language. It tells the database how to retrieve data, not just what you want.
Selection (σ) -  filters rows based on a condition. It's the relational algebra equivalent of a WHERE clause.
Projection (π) - Projection selects specific columns from a relation and drops the rest. It's how you trim a table down to only the attributes you care about.
Union (∪) - Union combines two relations into one, merging all their tuples. Duplicate rows get removed automatically.
Join (⋈) - put two relations on all attributes with the same name, and keeps only one copy of those shared columns in the result.
Rename (ρ)- Rename lets you give a relation or its attributes a new name. It doesn't change the data, just what things are called.

SQL query:

SELECT name
FROM customer
WHERE city = 'Bielefeld';

The correct relational algebra is:![SQL query result](pictures/workstream1-result.png)

- σ (Selection): Selects only customers from Bielefeld.
- π (Projection): Returns only their names.

## Studio Lab – LLM-Assisted SQL and Query Profiling

1. Exact prompt given to the LLM

For each city, return the number of distinct customers and the total revenue (qty × price) from orders placed in 2025. Sort by revenue from highest to lowest.

2. LLM-generated SQL

SELECT c.city,
       COUNT(DISTINCT c.customer_id) AS customers,
       SUM(ol.qty * p.price) AS revenue
FROM customer c
JOIN orders o
    ON o.customer_id = c.customer_id
JOIN order_line ol
    ON ol.order_id = o.order_id
JOIN product p
    ON p.product_id = ol.product_id
WHERE o.ordered_on >= '2025-01-01'
  AND o.ordered_on < '2026-01-01'
GROUP BY c.city
ORDER BY revenue DESC;

3. Predicted query plan

Before running EXPLAIN QUERY PLAN, the expected behaviour was:

SQLite would scan at least some tables, particularly order_line.

It would use primary-key lookups to retrieve matching orders, customers and products.

It might use temporary B-trees for grouping, distinct counting and sorting.

4. Actual EXPLAIN QUERY PLAN output

QUERY PLAN
|--SCAN ol
|--SEARCH o USING INTEGER PRIMARY KEY (rowid=?)
|--SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
|--SEARCH p USING INTEGER PRIMARY KEY (rowid=?)
|--USE TEMP B-TREE FOR GROUP BY
|--USE TEMP B-TREE FOR count(DISTINCT)
`--USE TEMP B-TREE FOR ORDER BY

5. Actual query results


6. Correctness and verification

The SQL query was executed successfully against the warehouse database. It returned four cities, counted distinct customers, calculated revenue using quantity multiplied by product price, filtered orders to 2025 and sorted revenue in descending order. The results and query plan were checked in SQLite. The output is consistent with the requested query.

## Task 2
## Preliminary Experiments
Index Experiment 1: orders(ordered_on)

Index created:

CREATE INDEX idx_orders_ordered_on
ON orders(ordered_on);

Expected benefit: Help SQLite filter orders by the 2025 date range.

Actual result: The query plan did not change. SQLite continued to scan order_line and search orders using its INTEGER PRIMARY KEY.

Conclusion: The date index was created successfully, but SQLite did not use it for this query. An index does not guarantee a faster query or a different execution plan.

Index Experiment 2: orders(customer_id)

Index created:

CREATE INDEX idx_orders_customer_id
ON orders(customer_id);

Expected benefit: Help SQLite find orders belonging to each customer.

Actual result: The query plan remained unchanged. SQLite continued to scan order_line and use primary-key lookups for orders, customers and products.

Conclusion: SQLite did not choose to use the customer ID index for this query. The index may be useful for other queries, but it did not improve the observed execution plan here.

Index Experiment 3: order_line(order_id)

Index created:

CREATE INDEX idx_order_line_order_id
ON order_line(order_id);

Actual query plan:

SEARCH o USING INDEX idx_orders_ordered_on (ordered_on>? AND ordered_on<?)
SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
SEARCH ol USING INDEX idx_order_line_order_id (order_id=?)
SEARCH p USING INTEGER PRIMARY KEY (rowid=?)
USE TEMP B-TREE FOR GROUP BY
USE TEMP B-TREE FOR count(DISTINCT)
USE TEMP B-TREE FOR ORDER BY

Observation: SQLite now uses the date index and the order-line index. The original full scan of order_line has disappeared.

Conclusion: These indexes changed the execution plan. This suggests a more targeted access strategy, although actual execution time must be measured before claiming a performance improvement.

## Index benchmark
Measurement	    Baseline	          After date index
Run 1	       0.205747 s	            0.236286 s
Run 2	       0.299851 s	            0.232572 s
Run 3	       0.228332 s	            0.225302 s
Median	       0.228332 s	            0.232572 s

Index	                Three run times (s)	           Median (s)	       Plan changed?
ix_orders_ordered_on   0.236286, 0.232572, 0.225302	    0.232572	             No
ix_orderline_order	   1.697717, 1.657577, 1.725880	    1.697717	             Yes
ix_orderline_product   1.625183, 1.685344, 1.879445	    1.685344	 No, compared with the preceding plan

The product index was not selected by SQLite for this dashboard query. The plan continued to use the date index and the order-line order_id index. The product table was accessed through its primary key. Therefore, adding an index on order_line(product_id) did not change this query plan.

Observation: The query became slower with the order-line index even though the plan used it. Record the measured times rather than claiming that the index improved performance.

## Step 4 Single-day lookup (without date index)

Query used:

SELECT o.order_id, o.ordered_on, c.name
FROM orders o
JOIN customer c ON c.customer_id = o.customer_id
WHERE o.ordered_on = '2026-02-14';

Baseline results (before recreating ix_orders_ordered_on):

Rows returned: 111

One-off SQLite runtime: 0.313088 seconds

Query plan:

SCAN o – SQLite scans the orders table.

SEARCH c USING INTEGER PRIMARY KEY (rowid=?) – SQLite finds each matching customer using the primary key.

Observation: Without the date index, SQLite scans the orders table to find orders for the requested date.

## Amortized benchmark – Before and after date index

Benchmark method:
Python script: Module03/bench.py
Repetitions per batch: 1,000
Number of batches: 3
Measurement: time.perf_counter()
Reported value: median milliseconds per query

Before date index:
Batch 1: 5.7128 ms/query
Batch 2: 5.9396 ms/query
Batch 3: 4.6386 ms/query
Median: 5.7128 ms/query
Query plan: SCAN o

After date index (ix_orders_ordered_on):
Batch 1: 0.3065 ms/query
Batch 2: 0.2908 ms/query
Batch 3: 0.2787 ms/query
Median: 0.2908 ms/query
Query plan: SEARCH o USING INDEX ix_orders_ordered_on (ordered_on=?)

Observation: The date index reduced the median query time from 5.7128 ms to 0.2908 ms, approximately 19.6 times faster. The query plan changed from a full table scan to an index search.

Conclusion: The date index is useful for this single-day lookup, even though it did not improve the original dashboard query.

## Step 5: Testing ix_orderline_product

Query tested:

EXPLAIN QUERY PLAN
SELECT *
FROM order_line ol
WHERE ol.product_id = 100;

Actual query plan:

SEARCH ol USING INDEX ix_orderline_product (product_id=?)

Observation: SQLite uses ix_orderline_product when filtering directly on order_line.product_id. The index is therefore useful for this query, even though it is not used by the dashboard query.

## Additional test: Effect of wrapping an indexed column in a function

Date index recreated:

CREATE INDEX ix_orders_ordered_on ON orders(ordered_on);

Function-wrapped query:

EXPLAIN QUERY PLAN
SELECT *
FROM orders
WHERE date(ordered_on) = '2026-02-14';

Result:

SCAN orders

Direct comparison:

EXPLAIN QUERY PLAN
SELECT *
FROM orders
WHERE ordered_on = '2026-02-14';

Result:

SEARCH orders USING INDEX ix_orders_ordered_on (ordered_on=?)

Observation: The ordinary index on ordered_on is used for direct equality, but not when ordered_on is wrapped in the date() function.

