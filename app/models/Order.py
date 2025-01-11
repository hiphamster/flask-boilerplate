from datetime import datetime

from sqlalchemy import (TIMESTAMP, Float, ForeignKey, Integer, String,
                        UniqueConstraint, func)
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel
from .Contact import Contact


class Order(BaseModel):

    __tablename__ = 'orders'

    #TODO defaults to: FirstnameLastnameMMDDYY
    name: Mapped[str] = mapped_column(String(100))

    contact_id: Mapped[int] = mapped_column(Integer, ForeignKey(Contact.id), nullable=False)

    order_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, 
                                                 server_default=func.now())

    #TODO set default close_date to order_date + 1 week
    close_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))

    stage_name: Mapped[str] = mapped_column(String(50), nullable=False,
                                            server_default='Order placed')

    order_total: Mapped[float] = mapped_column(Float, nullable=True)

    __table_args__ = (UniqueConstraint('contact_id', 'order_date', name='cid_odate'),)

    def __repr__(self):
        return f'Order: {self.name} id:{self.id}'
