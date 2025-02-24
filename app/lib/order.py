from typing import Optional

from flask import current_app
from sqlalchemy import and_, select

from app import db
from app.models import Order, Contact
from app.lib import Service

class OrderSvc(Service):

    Model = Order


    @classmethod
    def get_by_product(cls, product: str, excluisve: bool = False):
        """Return a list of orders for given product
           exclusive: if True, returns orders for with only
           one product.
        """
        pass
    # select
    #   id,
    #   name
    # from
    #   orders as o
    #   /* group by number of order_lines in order */
    #   inner join (
    #     select
    #       order_id,
    #       count(*) as ol_count
    #     from
    #       order_lines
    #     group by
    #       order_id
    #   ) as olc on o.id = olc.order_id
    #   /* only take those order_lines that match particular product */
    #   inner join (
    #     select
    #       order_id
    #     from
    #       order_lines ol
    #       join products p on ol.product_id = p.id
    #     where
    #       p.name = 'Trout HS'
    #   ) as f on o.id = f.order_id
    #   /* limit to orders with only one order_line */
    # where
    #   olc.ol_count = 1;    


    @classmethod
    def get_by_city(cls, city: str):
        """Return a list of orders for given city"""

        stmt = select(Order).join(
            Contact, Order.contact_id == Contact.id).where(
                Contact.city == city)
        return db.session.scalars(stmt)

       

    @classmethod
    def get_by_amount(cls, min:int, max:Optional[int]=None):
        pass

