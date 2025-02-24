
from  flask import current_app

from sqlalchemy import MetaData, Table, create_engine, select, update, delete, literal, and_, func, or_,text


DB_USER = 'koalaty'
DB_PASSWORD = 'eucalyptus'
DB_HOST = '127.0.0.1'
DB_PORT = 3307
DB_NAME = 'koalaty'
# DB_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DB_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_engine(DB_URL)
metadata = MetaData()

OrderLineTotals = Table('order_line_totals', metadata, autoload_with=engine)
Orders = Table('orders', metadata, autoload_with=engine)


#     select
#       olt.name,
#       round(sum(olt.quantity) / 16) as 'weight(lb)',
#       ceiling(sum(olt.quantity) / olt.average_weight) as pieces
#     from
#       order_line_totals olt
#       join orders o on olt.order_id = o.id
#     WHERE
#       o.stage_name like 'Order Placed'
#       or o.stage_name like 'Ready for pickup'
#     GROUP by
#       olt.name;

def open_orders_count():
    # select count(*) as 'open', stage_name from orders where stage_name in ('Order Placed','Ready for pickup');
    with engine.connect() as conn:
        r = conn.execute(
            text("select count(*) as 'open' from orders where stage_name in ('Order Placed','Ready for pickup')")).one()
        return r

def open_products():

    r =  None
    with engine.connect() as conn:
        stmt = select(OrderLineTotals.c.name,  
                      func.round(func.sum(OrderLineTotals.c.quantity)/16).label('weight'),
                      func.ceiling(func.sum(OrderLineTotals.c.quantity)/OrderLineTotals.c.average_weight).label('pieces')
                ).join(Orders, OrderLineTotals.c.order_id == Orders.c.id).where(
                    or_(Orders.c.stage_name == 'Order Placed', Orders.c.stage_name == 'Ready for pickup')
                ).group_by(OrderLineTotals.c.name)


        r = conn.execute(stmt).all()
        d = []
        current_app.logger.error('dummy')
        # current_app.logger.error(r)
        for prod in r:
            current_app.logger.error(f'{prod.name} {prod.weight} {prod.pieces}')
            d.append({'name': prod.name, 'weight': prod.weight, 'pieces': prod.pieces})
            # d.append({'name': prod['name'], 'weight': prod['weight'], 'pieces': prod['pieces']})           

    return d
#    return {
#        'title': 'Dashboard',
#        'clients': 100,
#        'orders': {'total': 800, 'open': 15}, 
#        'products': {'salmon': 9, 'trout': 12, 'branzino': 4}
#    }


