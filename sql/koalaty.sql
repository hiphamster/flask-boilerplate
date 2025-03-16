/* customer_name, order_date, order_lines, delivery_address, phone */
select
  olt.*
from
  order_line_totals olt
  join orders o on o.id = olt.order_id
where
  o.stage_name like 'Order Placed'
  or o.stage_name like 'Ready for pickup'
order by
  olt.order_date;
  
  
select
  olt.name,
  round(sum(olt.quantity) / 16) as 'weight(lb)',
  ceiling(sum(olt.quantity) / olt.average_weight) as pieces
from
  order_line_totals olt
  join orders o on olt.order_id = o.id
WHERE
  o.stage_name like 'Order Placed'
  or o.stage_name like 'Ready for pickup'
GROUP by
  olt.name;
  
  
select
  olt.*
from
  order_line_totals olt
  join orders o on olt.order_id = o.id
where
  o.stage_name in ('Ready for pickup')
  and olt.customer_name like 'Lidi%';


select
  olt.*
from
  order_line_totals olt
  join orders o on olt.order_id = o.id
where
  o.stage_name = 'Ready for pickup';
  
 
  
  
select

  concat(c.first_name, ' ', c.last_name) as name,
/*
  c.mobile_phone,
  
*/
  concat(c.street, ' ', c.city) as address,
  ort.customer_name,
  c.mobile_phone,
  round(sum(ort.order_line_total)) as total
FROM
  customers c
  join orders o on c.id = o.customer_id
  join order_line_totals ort on ort.order_id = o.id
WHERE
  o.stage_name in ('Order Placed','Ready for pickup')
group by ort.customer_name, concat(c.first_name, ' ', c.last_name), concat(c.street, ' ', c.city), c.mobile_phone;
  
  


select
  concat(c.first_name, ' ', c.last_name) as name,
  concat(c.street, ' ', c.city) as address,
  ort.customer_name,
  c.mobile_phone,
  round(sum(ort.order_line_total)) as total
FROM
  customers c
  join orders o on c.id = o.customer_id
  join order_line_totals ort on ort.order_id = o.id
WHERE
  year(o.order_date) = 2024 
AND
  month(o.order_date) = 12
group by ort.customer_name, concat(c.first_name, ' ', c.last_name), concat(c.street, ' ', c.city), c.mobile_phone;
    
  
  
  
select count(*) as 'open', stage_name from orders where stage_name in ('Order Placed','Ready for pickup');
  
  
  
  
  
  