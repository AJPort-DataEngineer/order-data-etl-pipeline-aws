SELECT 
  customer_id, 
  COUNT(order_id) AS total_orders, 
  SUM(total_amount) AS total_spent
FROM 
  orders_parquet_table
GROUP BY 
  customer_id
ORDER BY 
  total_orders DESC
LIMIT 10;
