from datetime import datetime

from sqlalchemy import JSON, TIMESTAMP, Integer, func, null
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

    def __repr__(self):
        return '<{}(id={self.id})>'.format(self.__class__.__name__, self=self)

