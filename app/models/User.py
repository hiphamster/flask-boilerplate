from flask_login import UserMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

from .BaseModel import BaseModel

# from app import db
# from datetime import datetime

class User(BaseModel, UserMixin):

    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(String(80), unique=False, nullable=False)
    email: Mapped[str]  = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), unique=False, nullable=False)
    # email_verified_at: Mapped[datetime] = mapped_column(DateTime, unique=False, nullable=True)

    @property
    def password(self):
        raise AttributeError('Password is not a readable property')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=10)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return '<User %r>' % self.name


