from math import ceil
from operator import eq
from typing import Optional

from flask import current_app
from sqlalchemy import and_, select

from app import db
# from app.models.Contact import Contact as mContact
# import app.models.Contact as mContact
from app.models import Contact as mContact


class Contact():
    model = mContact

    def __init__(self, *args, **kwargs):
        pass
    
    def _create(self, *args, **kwargs ):
        
        c = Contact.model(**kwargs)

        try:
            db.session.add(c)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)

    @staticmethod
    def create(first_name, last_name, email=None, mobile_phone=None,
               street=None, city=None, zipcode=None, extra=None):

        # pass in only ones with values
        c = mContact(**{k:v for k,v in locals().items() if v is not None})

        #XXX what Exception to catch? 
        db.session.add(c)
        db.session.commit()



    @staticmethod
    def update(id: int, first_name=None, last_name=None, email=None, mobile_phone=None,
               street=None, city=None, zipcode=None, extra=None):

        c = db.session.get(mContact, id)

        # pass in only ones with values
        c = mContact(**{k:v for k,v in locals().items() if v is not None})

        #XXX what Exception to catch? 
        db.session.add(c)
        db.session.commit()



    @staticmethod
    def get_by_id(id: int):
        """Retrieve a contact by unique ID"""
        return db.session.get(mContact, id)
        # return db.session.execute(select(Contact.model).where(Contact.model.id == id)).first()
    
    @staticmethod
    def get_by_name(name: Optional[str] = None, 
                    first_name: Optional[str] = None,
                    last_name: Optional[str] = None):
        """Retrieve contacts by name (multiple possible results)"""

        if (not name and not first_name and not last_name):
            return None

        if name:
            first_name,last_name = name.split(' ') 

        where = []

        if first_name:
            where.append(eq(mContact.first_name, first_name))

        if last_name:
            where.append((eq(mContact.last_name, last_name)))
        
        # use execute when not dealing with ORM objects (plain data select)
        # using list comprehension, to make it easier to access each entity 
        # TODO
        # a better idea is to return an actual entity if scalars() returns only 1
        # or a list otherwise
        return [c for c in db.session.scalars(select(mContact).where(*where)).all()]
    
    @staticmethod
    def get_by_phone(phone: str):
        """Retrieve a contact by phone number"""
        # return db.session.execute(select(Contact.model).where(Contact.model.mobile_phone == phone)).first()
        return db.session.scalars(select(Contact.model).where(Contact.model.mobile_phone == phone)).all()
    
    @staticmethod
    def get_by_email(email: str):
        """Retrieve a contact by email"""
        return db.session.execute(select(Contact.model).where(Contact.model.email == email)).first()
    
    @staticmethod
    def search(filters: dict):
        """Search for contacts based on multiple attributes"""
        pass
    
    @staticmethod
    def get_paginated(page: int = 1, page_size: int = 0):
        """Retrieve all contacts with pagination"""
        # offset((page - 1) * page_size)
        stmt = select(mContact).order_by(
                          mContact.last_name).limit(
                              page_size).offset(
                                  page_size * page - page_size) 

        count = mContact.count() or 0
        pages = ceil(count/page_size)

        # pages = count // page_size 
        # if count % page_size:
        #   pages += 1

        return {
            # number of records
            'count': count,
            # records per page
            'page_size': page_size,
            # number of pages
            'pages': pages, 
            # current page
            'page': page,
            # 'contacts': [obj for obj in db.session.scalars(stmt).all()]
            'contacts': db.session.scalars(stmt),
         }
        
    
    @staticmethod
    def get_contacts(filters: dict, sort_by: str = "name", order: str = "asc"):
        """Retrieve contacts with filtering and sorting"""
        pass
 


