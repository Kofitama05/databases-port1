import sqlite3
import time
import statistics
from pathlib import Path

DB = Path(__file__).with_name("warehouse.db")

SQL = """
SELECT o.order_id, o.ordered_on, c.name
FROM orders o
JOIN customer c ON c.customer_id = o.customer_id
WHERE o.ordered_on = '2026-02-14';
"""

N = 1000
BATCHES = 3


def show_plan(conn):
    print("\nQuery plan:")
    for row in conn.execute("EXPLAIN QUERY PLAN " + SQL):
        print(row)


def benchmark(conn, label):
    times = []

    # Warm-up: run once, but do not measure it.
    conn.execute(SQL).fetchall()

    for batch in range(BATCHES):
        start = time.perf_counter()

        for _ in range(N):
            conn.execute(SQL).fetchall()

        elapsed = time.perf_counter() - start
        ms_per_query = elapsed / N * 1000
        times.append(ms_per_query)

        print(f"{label} batch {batch + 1}: {ms_per_query:.4f} ms/query")

    print(f"{label} median: {statistics.median(times):.4f} ms/query")


with sqlite3.connect(DB) as conn:
    # Baseline: remove only the date index.
    conn.execute("DROP INDEX IF EXISTS ix_orders_ordered_on")

    print("=== BEFORE DATE INDEX ===")
    show_plan(conn)
    benchmark(conn, "Without date index")

    # Indexed condition: recreate the date index.
    conn.execute(
        "CREATE INDEX ix_orders_ordered_on ON orders(ordered_on)"
    )

    print("\n=== AFTER DATE INDEX ===")
    show_plan(conn)
    benchmark(conn, "With date index")

print("\nBenchmark complete.")
