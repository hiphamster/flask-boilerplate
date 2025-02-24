import json
from datetime import datetime

from flask import current_app
from sqlalchemy import JSON, TIMESTAMP, Integer, func, inspect, select
from sqlalchemy.orm import Mapped, mapped_column

from app import db


class BaseModel(db.Model):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                 server_default=func.now())

    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                 server_default=func.now(),
                                                 onupdate=func.now())

    extra: Mapped[dict] = mapped_column(JSON, nullable=True)


    @classmethod
    def count(cls):
        # return select(func.count(cls.id)).scalar_subquery()
        return db.session.scalar(select(func.count(cls.id)))

    def __repr__(self):
        return '<{}(id={self.id})>'.format(self.__class__.__name__, self=self)

    # @staticmethod
    def to_dict(self, include_relationships=False):
        """Convert a SQLAlchemy ORM selfect to a dictionary, with optional relationships."""

        inspection_obj = inspect(self)

        if inspection_obj:
            # data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
            data = {c.key: getattr(self, c.key) for c in inspection_obj.mapper.column_attrs}

            if include_relationships:
                # for rel in inspect(self).mapper.relationships:
                for rel in inspection_obj.mapper.relationships:
                    related_self = getattr(self, rel.key)
                    if related_self is not None:
                        if isinstance(related_self, list):  # One-to-Many
                            data[rel.key] = [BaseModel.to_dict(item) for item in related_self]
                        else:  # One-to-One
                            data[rel.key] = BaseModel.to_dict(related_self)
        
            return data

        else:
            msg = (f'Object {self} is not a valid '
                   f'ORM-mapped instance, calling ' 
                   f'"inspect(self)" returns None')

            current_app.logger.warning(msg)
            return {}


    def to_json(self, include_relationships=False):
        return json.dumps(BaseModel.to_dict(self, include_relationships), indent=4)  
