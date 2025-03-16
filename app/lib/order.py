from pprint import pformat
from typing import Optional

import sqlalchemy
from flask import current_app
from sqlalchemy import and_, select

from app import db
from app.lib import Service
from app.lib.exceptions import KoalatyException, RecordExistsException
from app.models import Contact, Order, OrderLine


class OrderSvc(Service):

    Model = Order


    @classmethod
    def get_by_product(cls, product: str, excluisve: bool = False):
        """Return a list of orders for given product
           exclusive: if True, returns orders for with only
           one product.
        """
        pass


    @classmethod
    def add_order(cls, _order: dict):
        """_order: session['current_order']"""

        order = cls.Model()
        order.order_date = _order['order_date'] # pyright: ignore
        order.contact = _order['contact'] # pyright: ignore
        order.order_lines = [] # pyright: ignore

        #TODO map _order ordler_line fields to OrderLine properties
        #TODO merge order_lines if the same product is selected


        try:
            db.session.add(order)
            db.session.commit()
            return order
        except sqlalchemy.exc.IntegrityError as e:
            current_app.logger.debug(f'IntegrityError: {pformat(e)}')
            raise RecordExistsException(f'Order exists')

            # print(e.orig.errno) # 1062
            # print(e.orig.sqlstate) # 23000
            # print(e.orig.msg)

        except sqlalchemy.exc.DBAPIError as e:
            current_app.logger.error(f'Database operation failed: {e}')
            raise KoalatyException('Database error')


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

