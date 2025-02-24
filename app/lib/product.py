from app import db
from app.lib import Service
from app.models import Product


class ProductSvc(Service):

    Model = Product

    @classmethod
    def get_by_city(cls, city: str):
        """Return a list of orders for given city"""
        pass


#        stmt = select(Order).join(
#            Contact, Order.contact_id == Contact.id).where(
#                Contact.city == city)
#        return db.session.scalars(stmt)
