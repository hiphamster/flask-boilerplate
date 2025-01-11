from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel


class Contact(BaseModel):

    __tablename__ = 'contacts'

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)

    last_name: Mapped[str] = mapped_column(String(50), nullable=False)

    email: Mapped[str] = mapped_column(String(100))

    mobile_phone: Mapped[str] = mapped_column(String(15))

    street: Mapped[str] = mapped_column(String(255))

    city: Mapped[str] = mapped_column(String(50))

    state: Mapped[str] = mapped_column(String(2))

    zipcode: Mapped[str] = mapped_column(String(5))

    personal_facebook_url: Mapped[str] = mapped_column(String(255))

    __table_args__ = (UniqueConstraint('first_name', 'last_name', 'mobile_phone',
                                       name='fname_lname_mphone'), )

    def __repr__(self):
        return f'Contact: {self.first_name} {self.last_name} id:{self.id}'
