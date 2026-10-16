-- Initialize 1,000,000 Orders for EXPLAIN ANALYZE Benchmarking
CREATE TABLE IF NOT EXISTS orders (
    id BIGSERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    total_amount NUMERIC(12, 2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    notes TEXT
);

-- Seed 1,000,000 synthetic rows with realistic distributions
-- Status: 70% 'COMPLETED', 20% 'PENDING', 9% 'PROCESSING', 1% 'REFUNDED'
INSERT INTO orders (customer_id, total_amount, status, created_at, notes)
SELECT
    (random() * 50000 + 1)::INT AS customer_id,
    round((random() * 950 + 50)::NUMERIC, 2) AS total_amount,
    CASE
        WHEN r < 0.70 THEN 'COMPLETED'
        WHEN r < 0.90 THEN 'PENDING'
        WHEN r < 0.99 THEN 'PROCESSING'
        ELSE 'REFUNDED'
    END AS status,
    NOW() - (random() * interval '365 days') AS created_at,
    'Order payload detail item: ' || md5(random()::text) AS notes
FROM (
    SELECT random() AS r FROM generate_series(1, 1000000)
) AS s;

-- Create target indices
CREATE INDEX idx_orders_customer_id ON orders (customer_id);
CREATE INDEX idx_orders_status ON orders (status);
CREATE INDEX idx_orders_created_at ON orders (created_at);

-- Mandatory: Collect database statistics for optimizer accuracy
ANALYZE orders;
