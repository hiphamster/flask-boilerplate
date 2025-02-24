from flask import current_app
from flask_migrate import current
from app.models import BaseModel
from typing import Type, TypeVar, Optional
from app import db
from sqlalchemy import select, ColumnElement
from math import ceil

# T will be any subclass of BaseModel
# T can be used to specify types in methods 
T = TypeVar('T', bound=BaseModel)

class Service():

    Model: Type[BaseModel]

    @classmethod
    def get_by_id(cls, id: int):
        return db.session.get(cls.Model,id) 


    @classmethod
    def get_by_name(cls, name: str):
        return db.session.get(cls.Model,name) 


    @classmethod
    def get_paginated(cls, order_by:Optional[Type[ColumnElement]], 
                      page: int = 1, page_size: int = 0):
        """Retrieve all contacts with pagination"""

        current_app.logger.debug(f'cls: {cls}')


        # offset((page - 1) * page_size)
        stmt = select(cls.Model).order_by(order_by).limit(
            page_size).offset(page_size * page - page_size) 

        current_app.logger.debug(f'stmt sql: {stmt}')

        count = cls.Model.count() or 0
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
            'instances': db.session.scalars(stmt),
         }

