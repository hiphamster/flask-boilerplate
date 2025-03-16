from math import ceil
from operator import eq
from pprint import pformat
from typing import Optional

import sqlalchemy
from flask import current_app
from sqlalchemy import select

from app import db
from app.lib import Service
from app.lib.exceptions import KoalatyException, RecordExistsException
from app.models import Contact

class ContactSvc(Service):
    Model = Contact

    @classmethod
    def add_contact(cls, form_data: dict ):

        c = cls.Model()

        c.first_name = form_data['fname']               # pyright: ignore
        c.last_name = form_data['lname']                # pyright: ignore
        c.email = form_data['email']                    # pyright: ignore
        c.mobile_phone = form_data['mobile_phone']      # pyright: ignore
        c.street = form_data['street']                  # pyright: ignore
        c.city = form_data['city']                      # pyright: ignore
        c.state = form_data['state']                    # pyright: ignore
        c.zipcode = form_data['zipcode']                # pyright: ignore
        c.personal_facebook_url = form_data['fb_url']   # pyright: ignore

        try:
            db.session.add(c)
            db.session.commit()
            return c
        except sqlalchemy.exc.IntegrityError as e:
            current_app.logger.debug(f'IntegrityError: {pformat(e)}')
            raise RecordExistsException(f'This product already exists')

            # print(e.orig.errno) # 1062
            # print(e.orig.sqlstate) # 23000
            # print(e.orig.msg)

        except sqlalchemy.exc.DBAPIError as e:
            current_app.logger.error(f'Database operation failed: {e}')
            raise KoalatyException('Database error')

        except Exception as e:
            current_app.logger.error(f'Operation failed: {e}')
            raise KoalatyException('Operation failed: {e}')


    @classmethod
    def update_contact(cls, id: int, form_data: dict):
        pass

    @classmethod
    def id_name_list(cls):
        try:
            stmt = select(cls.Model.id, cls.Model.full_name).order_by(cls.Model.full_name) # pyright: ignore
            return [(k,v) for (k,v) in db.session.execute(stmt).all()]

        except sqlalchemy.exc.DBAPIError as e:
            current_app.logger.error(f'Database operation failed: {e}')
            raise KoalatyException('Database error')

        except Exception as e:
            current_app.logger.error(f'Operation failed: {e}')
            raise KoalatyException('Operation failed: {e}')


#    #TODO needs to match super().get_by_name()
#    @classmethod
#    def _get_by_name(cls, name: Optional[str] = None,
#                    first_name: Optional[str] = None,
#                    last_name: Optional[str] = None):
#        """Retrieve contacts by name (multiple possible results)"""
#
#        if (not name and not first_name and not last_name):
#            return None
#
#        if name:
#            first_name, last_name = name.split(' ')
#
#        where = []
#
#        if first_name:
#            where.append(eq(cls.Model.first_name, first_name))
#
#        if last_name:
#            where.append((eq(cls.Model.last_name, last_name)))
#
#        # use execute when not dealing with ORM objects (plain data select)
#        # using list comprehension, to make it easier to access each entity
#        # TODO
#        # a better idea is to return an actual entity if scalars() returns only 1
#        # or a list otherwise
#        return [c for c in db.session.scalars(select(cls.Model).where(*where)).all()]
#
#    @classmethod
#    def get_by_phone(cls, phone: str):
#        """Retrieve a contact by phone number"""
#        # return db.session.execute(select(Contact.model).where(Contact.model.mobile_phone == phone)).first()
#        return db.session.scalars(
#            select(cls.Model).where(
#                cls.Model.mobile_phone == phone)).all()
#
#    @classmethod
#    def get_by_email(cls, email: str):
#        """Retrieve a contact by email"""
#        return db.session.execute(
#            select(cls.Model).where(cls.Model.email == email)).first()
#
#    @classmethod
#    def search(cls, filters: dict):
#        """Search for contacts based on multiple attributes"""
#        pass
#
#    @classmethod
#    def _get_paginated(cls, page: int = 1, page_size: int = 0):
#        """Retrieve all contacts with pagination"""
#        # offset((page - 1) * page_size)
#        stmt = select(cls.Model).order_by(
#            cls.Model.last_name).limit(page_size).offset(page_size * page -
#                                                        page_size)
#
#        count = cls.Model.count() or 0
#        pages = ceil(count / page_size)
#
#        # pages = count // page_size
#        # if count % page_size:
#        #   pages += 1
#
#        paginated = {
#            # number of records
#            'count': count,
#            # records per page
#            'page_size': page_size,
#            # number of pages
#            'pages': pages,
#            # current page
#            'page': page,
#            # 'contacts': [obj for obj in db.session.scalars(stmt).all()]
#            'contacts': db.session.scalars(stmt),
#        }
#
#        return paginated
#        
#
#    @classmethod
#    def get_contacts(cls, filters: dict, sort_by: str = "name", order: str = "asc"):
#        """Retrieve contacts with filtering and sorting"""
#        pass
