WITH order_totals AS (
  SELECT
    o.id as order_id,
    concat(c.first_name, ' ', c.last_name) AS customer_name,
    o.order_date,
    SUM(ol.quantity * p.unit_price) AS total_amount
  FROM
    orders o
    JOIN customers c ON o.customer_id = c.id
    JOIN order_lines ol ON ol.order_id = o.id
    JOIN products p ON ol.product_id = p.id
  WHERE
    year(o.order_date) = 2025
    AND month(o.order_date) = 1
    /* AND o.stage_name not like 'Closed - Lost'*/
  GROUP BY
    o.id,
    customer_name,
    o.order_date
),
order_line_details AS (
  SELECT
    o.id as order_id,
    NULL AS customer_name,
    NULL AS order_date,
    ol.id as order_line_id,
    p.name AS product_name,
    ol.quantity,
    p.unit_price,
    (ol.quantity * p.unit_price) AS order_line_total
  FROM
    orders o
    JOIN order_lines ol ON o.id = ol.order_id
    JOIN products p ON ol.product_id = p.id
  WHERE
    year(o.order_date) = 2025
    AND month(o.order_date) = 1
    /* AND o.stage_name not like 'Closed - Lost'*/
)
SELECT
  order_id,
  customer_name,
  order_date,
  NULL AS order_line_id,
  NULL AS product_name,
  NULL AS qty,
  NULL AS unit_price,
  total_amount AS amount
FROM
  order_totals
UNION ALL
SELECT
  order_id,
  customer_name,
  order_date,
  order_line_id,
  product_name,
  quantity,
  unit_price,
  order_line_total AS amount
FROM
  order_line_details
ORDER BY
  order_id,
  order_line_id