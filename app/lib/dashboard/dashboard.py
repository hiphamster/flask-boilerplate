from os import stat

from werkzeug.datastructures.structures import _OrderedMultiDict
from . import engine as koalaty_engine, Orders, OrderLineTotals
from sqlalchemy import text, func, select, or_
from flask import current_app
from app import db
from collections import defaultdict



class Dashboard():

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def open_order_count():
        """Number of open orders"""
        with koalaty_engine.connect() as conn:
            stmt = select(
                func.count(Orders.c.id).label('open')).where(
                    Orders.c.stage_name.in_(['Order Placed', 'Ready for pickup']))
            r = conn.execute(stmt).one()
            return r


    @staticmethod
    def open_order_count_by_product():
        """Number of orders for each product"""
        with koalaty_engine.connect() as conn:
            stmt = select(
                OrderLineTotals.c.name.label('product'),
                func.count(Orders.c.id).label('count')
            ).join(Orders,  OrderLineTotals.c.order_id == Orders.c.id ).where(
                    Orders.c.stage_name.in_(
                        ['Order Placed','Ready for pickup'])
                ).group_by(OrderLineTotals.c.name)
            r = conn.execute(stmt).all()
            return {p.product: p for p in r} 

    @staticmethod
    def products_by_open_orders():
        """Products that have been ordered"""
        pass    


    @staticmethod
    def products_to_customers():
        """Products to customers mapping"""

        with koalaty_engine.connect() as conn:
            stmt = select(OrderLineTotals.c.customer_name, 
                          OrderLineTotals.c.name.label('product'),
                          func.ceiling(
                                  OrderLineTotals.c.quantity / OrderLineTotals.c.average_weight
                          ).label('pieces'),
                          OrderLineTotals.c.quantity.label('weight')).join(
                              Orders, OrderLineTotals.c.order_id == Orders.c.id
                          ).where(
                            Orders.c.stage_name.in_(['Order Placed', 'Ready for pickup']))

            r = conn.execute(stmt).all()

            # c2p = defaultdict(list)
            c2p = dict()
            p2c = defaultdict(list)

            for rec in r:
                p2c[rec.product].append(rec.customer_name)

                # 'customer_name': ['prod1','prod2']
                # c2p[rec.customer_name].append(rec.product)

                c2p[rec.customer_name] = c2p.get(rec.customer_name, {})
                c2p[rec.customer_name][rec.product] = (rec.weight, rec.pieces)


            current_app.logger.error(f'MAPPINGS: \n{[dict(c2p),dict(p2c)]}')

            return {'customer_to_product': dict(c2p), 'product_to_customer': dict(p2c)}



    @staticmethod
    def open_orders_product_qty():
        """Products ordered, with weight and pieces"""

        with koalaty_engine.connect() as conn:
            stmt = select(OrderLineTotals.c.name,  
                          func.round(func.sum(OrderLineTotals.c.quantity)/16).label('weight'),
                          func.ceiling(func.sum(
                                  OrderLineTotals.c.quantity)/OrderLineTotals.c.average_weight
                          ).label('pieces')
                    ).join(Orders, OrderLineTotals.c.order_id == Orders.c.id).where(
                        Orders.c.stage_name.in_(['Order Placed','Ready for pickup'])
                    ).group_by(OrderLineTotals.c.name)

            r = conn.execute(stmt).all()
            current_app.logger.error(f'oo_product_qty: \n{r}')

            # out = [{'name': p.name, 'weight': p.weight, 'pieces': p.pieces} for p in r]
            # product_stats = defaultdict(list)
            
            return {p.name: p for p in r}


    # select olt.customer_name, olt.name as 'product', ceiling(olt.quantity / olt.average_weight) as 'pieces', olt.quantity as 'weight' from order_line_totals olt join orders o on olt.order_id = o.id 
    # where o.stage_name in ('Order Placed','Ready for pickup');



def test():
    with koalaty_engine.connect() as conn:
        r = conn.execute(text(f'select count(*) as "count" from orders')).one()
        current_app.logger.error(f'Orders count: {r.count}')




