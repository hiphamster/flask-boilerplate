insert into
  contacts(
    first_name,
    last_name,
    email,
    mobile_phone,
    street,
    city,
    state,
    zipcode,
    personal_facebook_url
  )
select
  first_name,
  last_name,
  email,
  mobile_phone,
  street,
  city,
  state,
  zip,
  personal_facebook_url
from
  koalaty.customers;
select
  month(order_date)
from
  orders
limit
  5;
truncate table contacts;
set
  foreign_key_checks = 0;
truncate table orders;
truncate table contacts;
commit;
set
  foreign_key_checks = 1;
select
  o.*
from
  orders o
  join order_lines ol on o.id = ol.order_id
  join products p on ol.product_id = p.id
where
  p.name like 'Trout HS';
select
  o.id,
  o.name
from
  orders o
  join order_lines ol on o.id = ol.order_id
GROUP by
  o.id
having
  count(DISTINCT(ol.product_id)) = 1;
select
  id,
  name
from
  orders as p
  inner join (
    select
      order_id,
      count(*) as c_count
    from
      order_lines
      join products on order_lines.product_id = products.id
      /*where products.name = 'Trout HS'*/
    GROUP by
      order_id
  ) as c on p.id = c.order_id
where
  c.c_count = 1;
select
  order_id,
  count(*)
from
  order_lines
group by
  order_id;
select
  id,
  name
from
  orders as o
  inner join (
    select
      order_id,
      count(*) as ol_count
    from
      order_lines
    group by
      order_id
  ) as olc on o.id = olc.order_id
where
  olc.ol_count = 1;
select
  ol.order_id
from
  order_lines ol
  join products p on ol.product_id = p.id
where
  p.name = 'Trout HS';
  
  
  
  
  
  
  
  
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
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  