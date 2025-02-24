from sqlalchemy import Float, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .BaseModel import BaseModel
from .Order import Order
from .Product import Product


class OrderLine(BaseModel):

    __tablename__ = 'order_lines'

    order_id: Mapped[int] = mapped_column(Integer, ForeignKey(Order.id), nullable=False)

    product_id: Mapped[int] = mapped_column(Integer, ForeignKey(Product.id), nullable=False)

    quantity: Mapped[int] = mapped_column(Integer)

    # bidirectional relationship
    order: Mapped["Order"] = relationship(back_populates="order_lines")

    product: Mapped["Product"] = relationship()


    #XXX probably not needed, as
    total: Mapped[float] = mapped_column(Float, nullable=True)

    __table_args__ = (UniqueConstraint('order_id', 'product_id', name='oid_pid'),)

    def __repr__(self):
        return f'OrderLine id:{self.id}'
