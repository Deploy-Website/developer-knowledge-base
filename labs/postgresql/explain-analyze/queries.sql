-- ==============================================================================
-- Lab: PostgreSQL EXPLAIN ANALYZE Verification Queries
-- Database: knowledgedb
-- ==============================================================================

\echo '--- Scenario 1: Unindexed / Low-selectivity query -> Sequential Scan ---'
EXPLAIN (ANALYZE, BUFFERS)
SELECT count(*) 
FROM orders 
WHERE notes LIKE '%abcde%';

\echo '--- Scenario 2: High Selectivity query -> Index Scan ---'
-- Querying a specific customer (1M rows / 50k customers = ~20 rows per customer = 0.002% selectivity)
EXPLAIN (ANALYZE, BUFFERS)
SELECT * 
FROM orders 
WHERE customer_id = 4289;

\echo '--- Scenario 3: Moderate Selectivity query -> Bitmap Index & Heap Scan ---'
-- 'REFUNDED' status is ~1% of 1,000,000 rows (~10,000 rows)
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, customer_id, total_amount, status 
FROM orders 
WHERE status = 'REFUNDED';

\echo '--- Scenario 4: Work Mem Spillover -> External Merge Sort vs Quicksort in Memory ---'
-- Part 4A: work_mem constricted to 64kB to force disk spill
SET work_mem = '64kB';
EXPLAIN (ANALYZE, BUFFERS)
SELECT * 
FROM orders 
ORDER BY total_amount DESC 
LIMIT 5000;

-- Part 4B: work_mem expanded to 16MB to stay purely in RAM
SET work_mem = '16MB';
EXPLAIN (ANALYZE, BUFFERS)
SELECT * 
FROM orders 
ORDER BY total_amount DESC 
LIMIT 5000;

\echo '--- Scenario 5: Safe Production DML Mutation Analysis with Rollback ---'
BEGIN;
EXPLAIN (ANALYZE, BUFFERS)
DELETE FROM orders 
WHERE status = 'REFUNDED' 
  AND created_at < NOW() - INTERVAL '300 days';
ROLLBACK; -- Critical: guarantees zero data corruption during testing
