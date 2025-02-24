from datetime import datetime
from typing import List

from sqlalchemy import (TIMESTAMP, Float, ForeignKey, Integer, String,
                        UniqueConstraint, func)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import BaseModel, Contact


class Order(BaseModel):

    __tablename__ = 'orders'

    #TODO defaults to: FirstnameLastnameMMDDYY
    name: Mapped[str] = mapped_column(String(100))

    contact_id: Mapped[int] = mapped_column(Integer,
                                            ForeignKey(Contact.id),
                                            nullable=False)
    # bidirectional relationship
    contact: Mapped["Contact"] = relationship(back_populates="orders")

    order_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                 nullable=False,
                                                 server_default=func.now())

    #TODO set default close_date to order_date + 1 week
    close_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))

    stage_name: Mapped[str] = mapped_column(String(50),
                                            nullable=False,
                                            server_default='Order placed')

    order_total: Mapped[float] = mapped_column(Float, nullable=True)


    # bidirectional relationship
    order_lines: Mapped[List["OrderLine"]] = relationship(back_populates="order")

    #XXX To be canged when proper order pricing is done
    @property
    def computed_total(self):
        _sum = 0
        for ol in self.order_lines:
            _sum += ol.quantity * ol.product.unit_price
        return _sum

    __table_args__ = (UniqueConstraint('contact_id', 'order_date', name='cid_odate'),)

    def __repr__(self):
        return f'Order: {self.name} id:{self.id}'
