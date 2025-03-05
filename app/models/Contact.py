from typing import List

from sqlalchemy import Computed, String, UniqueConstraint, func
# from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from .BaseModel import BaseModel
from app.models import BaseModel


class Contact(BaseModel):

    __tablename__ = 'contacts'

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)

    last_name: Mapped[str] = mapped_column(String(50), nullable=False)

    full_name: Mapped[str] = mapped_column(String(101), Computed(
        func.concat(first_name, ' ', last_name), persisted=False), nullable=True)

    email: Mapped[str] = mapped_column(String(100), nullable=True)

    mobile_phone: Mapped[str] = mapped_column(String(15), nullable=True)

    street: Mapped[str] = mapped_column(String(255), nullable=True)

    city: Mapped[str] = mapped_column(String(50), nullable=True)

    state: Mapped[str] = mapped_column(String(2), nullable=True)

    zipcode: Mapped[str] = mapped_column(String(5), nullable=True)

    personal_facebook_url: Mapped[str] = mapped_column(String(255), nullable=True)

    # bidirectional relationship
    orders: Mapped[List["Order"]] = relationship(back_populates="contact") # pyright: ignore


    @property
    def order_count(self):
        return len(self.orders) if self.orders else 0

    __table_args__ = (UniqueConstraint('first_name', 'last_name', 'mobile_phone',
                                       name='fname_lname_mphone'), )

    def __repr__(self):
        return f'Contact: {self.first_name} {self.last_name} id:{self.id}'
