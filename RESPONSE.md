## Q1: What is the GIL in Python?

The (Global Interpreter Lock) is a mutex (or a lock) that allows only one thread to execute in the Python interpreter at any given time, even in multi-threaded programs.


Pros of GIL:

- Simplifies memory management in CPython
- Makes single-threaded programs faster by avoiding lock overhead
- Prevents race conditions in reference counting
- Makes C extensions easier to write

Cons of GIL:

- Limits true parallel execution in multi-threaded programs
- Can become a bottleneck in CPU-bound multi-threaded applications
- Doesn't take full advantage of multi-core systems for CPU-bound tasks





## Q3: How to optimize a slow SQL SELECT query?

When facing slow SQL SELECT performance, here’s a step-by-step strategy:

---

-Application-level caching:
   - Implement caching for frequently accessed data
   - Use Redis or Memcached for query result caching

 -Optimize the query:
   - Select only needed columns instead of `SELECT *`
   - Avoid subqueries when joins would be more efficient
   - Use appropriate join types

-Database optimization:
   - Update statistics with `ANALYZE`
   - Consider table partitioning for large tables
   - Adjust database configuration parameters
-Analyze the query:
   - Use `EXPLAIN ANALYZE` to understand the execution plan
   - Identify full table scans, missing indexes, or inefficient joins
-Add appropriate indexes:
   - Create indexes on columns used in WHERE, JOIN, and ORDER BY clauses
   - Consider composite indexes for frequently queried column combinations

---
