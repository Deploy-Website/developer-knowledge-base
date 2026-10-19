# Raw Incident Note: PostgreSQL API Hanging Due to Exclusive Lock

- **Ngày ghi nhận**: 2026-10-14
- **Dự án**: Core Payment API
- **Chủ đề**: PostgreSQL
- **Mô tả hiện tượng**:
  - Đột nhiên API endpoint `/api/v1/orders/checkout` bị timeout 504 hàng loạt.
  - Connection pool HikariCP báo `Connection is not available, request timed out after 30005ms`.
  - Kiểm tra database CPU rất thấp (< 10%), nhưng số lượng active connections chạm trần `max_connections = 200`.

- **Các câu lệnh đã chạy để debug trong console psql**:
  ```sql
  -- Xem các query đang bị chặn (blocking / waiting)
  SELECT pid, usename, state, wait_event_type, wait_event, query, now() - query_start AS duration
  FROM pg_stat_activity
  WHERE wait_event_type = 'Lock'
  ORDER BY duration DESC;

  -- Tìm PID gây nghẽn
  SELECT blocked_locks.pid     AS blocked_pid,
         blocking_locks.pid    AS blocking_pid,
         blocked_activity.query AS blocked_statement,
         blocking_activity.query AS current_statement_in_blocking_process
  FROM pg_catalog.pg_locks blocked_locks
  JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
  JOIN pg_catalog.pg_locks blocking_locks 
      ON blocking_locks.locktype = blocked_locks.locktype
      AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
      AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
      AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page
      AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple
      AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid
      AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid
      AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
      AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
      AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid
      AND blocking_locks.pid != blocked_locks.pid
  JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
  WHERE NOT blocked_locks.granted;
  ```

- **Nguyên nhân tìm ra**:
  - Kỹ sư chạy một lệnh `ALTER TABLE orders ADD COLUMN is_vip BOOLEAN DEFAULT FALSE;` trực tiếp trong giờ cao điểm mà không set `lock_timeout`.
  - Dù Postgres 11+ add column có default không rewrite bảng, nhưng lệnh `ALTER TABLE` vẫn yêu cầu `ACCESS EXCLUSIVE` lock.
  - Lệnh này phải xếp hàng sau một query `SELECT` dài 20 giây.
  - Toàn bộ các câu `SELECT` và `INSERT` mới tiếp theo lại phải xếp hàng sau lệnh `ALTER TABLE` này (Lock Queue FIFO starvation).

- **Biện pháp xử lý ngay lập tức**:
  - Chạy `SELECT pg_cancel_backend(blocking_pid);` hoặc `SELECT pg_terminate_backend(blocking_pid);`.
- **Giải pháp phòng ngừa lâu dài**:
  - Luôn set `lock_timeout = '2s'` trước khi chạy bất kỳ câu lệnh DDL nào.
  - Bật `idle_in_transaction_session_timeout = '30s'`.
  - Kiểm tra transaction isolation và sử dụng batching.
