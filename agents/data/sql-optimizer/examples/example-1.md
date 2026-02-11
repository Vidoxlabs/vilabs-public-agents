# Example: Slow Query Optimization

## Input

A slow query affecting application performance that needs analysis and optimization.

**Original Query**:

```sql
SELECT u.id, u.email, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY u.id
HAVING COUNT(o.id) > 5
ORDER BY order_count DESC;
```

**Performance Baseline**:

- Execution Time: 8.5 seconds
- Rows Returned: ~2,500
- Database: MySQL 8.0 with 500k users, 5M orders

## Output

### 📊 Query Analysis Report

**Query ID**: orders_by_recent_users
**Database**: MySQL 8.0
**Execution Time**: 8.5 seconds (baseline)
**Rows Examined**: 1.2M
**Rows Returned**: 2,500

#### 🔍 Performance Issues Identified

**High Priority** 🔴

1. **Missing Index on `orders.user_id`**
   - Issue: FK column not indexed, causing full table scan
   - Impact: 4.2 seconds of 8.5s total time
   - Fix: `CREATE INDEX idx_orders_user_id ON orders(user_id);`

2. **Suboptimal Join Strategy**
   - Issue: LEFT JOIN converts to nested loop with no index optimization
   - Impact: Additional 2.1 seconds from repeated lookups
   - Fix: Add index on join columns

**Medium Priority** 🟡

3. **Full Table Scan on users Table**
   - Issue: `created_at` filter lacks index
   - Impact: ~1.2 seconds reading unnecessary user records
   - Fix: `CREATE INDEX idx_users_created_at ON users(created_at DESC);`

4. **Inefficient GROUP BY**
   - Issue: Grouping happens after full join completion
   - Impact: Processing unnecessary rows before filtering
   - Fix: Reorder operations or use temporary table

#### 📈 Execution Plan Analysis

**Current Plan** (8.5 seconds):

```
1. Table Scan: users (500k rows examined)
   - Filter: created_at > DATE_SUB(NOW(), INTERVAL 30)
   - Rows: ~125k after filter

2. Nested Loop Join: orders
   - For each user: scan orders table (no index)
   - Full table scan per iteration (5M rows per user)

3. GROUP BY: aggregate counts
4. HAVING: filter by count > 5
5. ORDER BY: sort results
```

#### ✅ Optimized Query

```sql
-- Version 1: With proper indexing (Recommended)
SELECT u.id, u.email, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY u.id, u.email
HAVING COUNT(o.id) > 5
ORDER BY order_count DESC;

-- Version 2: Using temporary table (Alternative)
CREATE TEMPORARY TABLE recent_users AS
SELECT id, email
FROM users
WHERE created_at > DATE_SUB(NOW(), INTERVAL 30 DAY);

SELECT ru.id, ru.email, COUNT(o.id) as order_count
FROM recent_users ru
LEFT JOIN orders o ON ru.id = o.user_id
GROUP BY ru.id, ru.email
HAVING COUNT(o.id) > 5
ORDER BY order_count DESC;

-- Version 3: Using subquery with COUNT (Most efficient)
SELECT u.id, u.email, order_counts.cnt as order_count
FROM users u
JOIN (
  SELECT user_id, COUNT(*) as cnt
  FROM orders
  GROUP BY user_id
  HAVING COUNT(*) > 5
) order_counts ON u.id = order_counts.user_id
WHERE u.created_at > DATE_SUB(NOW(), INTERVAL 30 DAY)
ORDER BY order_count DESC;
```

#### 🗂️ Index Strategy

**Recommended Indexes**:

| Index                     | Columns                     | Type      | Rationale                |
| ------------------------- | --------------------------- | --------- | ------------------------ |
| `idx_users_created_at`    | users(created_at DESC)      | BTM       | Filter on date range     |
| `idx_orders_user_id`      | orders(user_id)             | BTM       | JOIN condition (FK)      |
| `idx_orders_user_created` | orders(user_id, created_at) | Composite | Potential covering index |

**Implementation**:

```sql
CREATE INDEX idx_users_created_at ON users(created_at DESC);
CREATE INDEX idx_orders_user_id ON orders(user_id);
-- Analyze table after index creation
ANALYZE TABLE users;
ANALYZE TABLE orders;
```

#### 📊 Performance Comparison

| Metric         | Original | Optimized | Improvement    |
| -------------- | -------- | --------- | -------------- |
| Execution Time | 8.5s     | 0.34s     | **96% faster** |
| Rows Examined  | 1.2M     | 78k       | **98% fewer**  |
| Rows Returned  | 2,500    | 2,500     | Same           |
| Memory Usage   | 45MB     | 8MB       | 82% less       |

#### 🔧 Query Tuning Steps

1. **Add Indexes**

   ```sql
   CREATE INDEX idx_users_created_at ON users(created_at DESC);
   CREATE INDEX idx_orders_user_id ON orders(user_id);
   ```

2. **Update Statistics**

   ```sql
   ANALYZE TABLE users;
   ANALYZE TABLE orders;
   ```

3. **Rewrite Query** (use Version 3 above)

4. **Verify Execution Plan**
   ```sql
   EXPLAIN FORMAT=JSON
   SELECT u.id, u.email, order_counts.cnt as order_count
   FROM users u
   JOIN (
     SELECT user_id, COUNT(*) as cnt
     FROM orders
     GROUP BY user_id
     HAVING COUNT(*) > 5
   ) order_counts ON u.id = order_counts.user_id
   WHERE u.created_at > DATE_SUB(NOW(), INTERVAL 30 DAY)
   ORDER BY order_count DESC;
   ```

#### 💡 General Optimization Recommendations

1. **Regular Index Maintenance**: Rebuild fragmented indexes monthly
2. **Query Caching**: Consider caching results for read-heavy queries
3. **Partitioning**: Partition orders table by date for better scans
4. **Archive Old Data**: Move records older than 1 year to archive table
5. **Query Monitoring**: Set up slow query logs to catch patterns

#### 🚨 Prevention Checklist

- [ ] All JOIN columns have indexes
- [ ] ORDER BY columns are indexed
- [ ] WHERE clause filters use indexed columns
- [ ] No function calls on indexed columns in WHERE clause
- [ ] Execution plan shows index usage (no table scans)
- [ ] Statistics are current
- [ ] Test with realistic data volume

## Context

This example demonstrates:

- Identifying missing indexes causing performance issues
- Analyzing execution plans to find bottlenecks
- Multiple optimization approaches (indexing, query rewrite, temp tables)
- Quantifying improvements with metrics
- Providing implementation steps
- Preventive recommendations

## Effectiveness

- **Issues Identified**: ✓ 4 critical issues found
- **Performance Gain**: ✓ 96% faster execution
- **Actionable**: ✓ Specific implementation steps provided
- **Best Practices**: ✓ Index strategy and maintenance guidance

**Notes**: This optimization achieves significant performance improvements through proper indexing and query restructuring, demonstrating the importance of query analysis in database performance.
