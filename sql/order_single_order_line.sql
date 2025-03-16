select
  id,
  name
from
  orders as o
  /* group by number of order_lines in order */
  inner join (
    select
      order_id,
      count(*) as ol_count
    from
      order_lines
    group by
      order_id
  ) as olc on o.id = olc.order_id
  /* only take those order_lines that match particular product */
  inner join (
    select
      order_id
    from
      order_lines ol
      join products p on ol.product_id = p.id
    where
      p.name = 'Trout HS'
  ) as f on o.id = f.order_id
  /* limit to orders with only one order_line */
where
  olc.ol_count = 1;
  
