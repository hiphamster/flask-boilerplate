import sqlalchemy
from flask import current_app
from app import db
from app.lib.exceptions import KoalatyException, RecordExistsException
from app.lib import Service
from app.models import Product

import app.lib
from pprint import pformat


class ProductSvc(Service):

    Model = Product

    @classmethod
    def get_by_city(cls, city: str):
        """Return a list of orders for given city"""
        pass

    @classmethod
    def add_product(cls, form_data: dict):

        p = Product()
        p.name = form_data['name']
        p.description = form_data['desc']
        p.average_weight = form_data['avg_weight']
        p.unit_price = form_data['unit_price']
        db.session.add(p)

        try:
            db.session.commit()
            return p

        except sqlalchemy.exc.IntegrityError as e:
            current_app.logger.debug(f'IntegrityError: {pformat(e)}')
            raise RecordExistsException(f'This product already exists')

            # record exists
#            if (e.orig.errno == 1062 and e.orig.sqlstate == '23000'):
#                current_app.logger.warning(f'Record exists - {p}')
#                raise RecordExistsException(f'This product already exists')
#                # print(e.orig.errno) # 1062
#                # print(e.orig.sqlstate) # 23000
#                # print(e.orig.msg)

# current_app.logger.error(f'Database operation failed: {e}')
# raise app.lib.KoalatyException('Database error')

        except sqlalchemy.exc.DBAPIError as e:
            current_app.logger.error(f'Database operation failed: {e}')
            raise app.lib.KoalatyException('Database error')

        except Exception as e:
            current_app.logger.error(f'Operation failed: {e}')
            raise app.lib.KoalatyException('Operation failed: {e}')


#        stmt = select(Order).join(
#            Contact, Order.contact_id == Contact.id).where(
#                Contact.city == city)
#        return db.session.scalars(stmt)
