from .BaseModel import BaseModel
from enum import Enum

from sqlalchemy import (Float, Integer, String)
from sqlalchemy import Enum as SQAEnum
from sqlalchemy.orm import Mapped, mapped_column


class ProductWeight(Enum):
    POUNDS = 'lb'
    KILOGRAMS = 'kg'
    OUNCES = 'oz'
    GRAMS = 'g'
    EACH = 'ea'
    # PERCENT = '%'


class Product(BaseModel):

    __tablename__ = 'products'

    name: Mapped[str] = mapped_column(String(30), unique=True)
    description: Mapped[str] = mapped_column(String(100), nullable=True)
    #TODO change OUNCES to OZ
    units: Mapped[ProductWeight] = mapped_column(SQAEnum(ProductWeight), server_default='OUNCES',
                                                 nullable=False)
    unit_price: Mapped[float] = mapped_column(Float)
    average_weight: Mapped[int] = mapped_column(Integer)

    def __repr__(self):
        return f'Product:{self.name} id:{self.id}'
