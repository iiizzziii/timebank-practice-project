from sqlalchemy.orm import relationship

from timebank.models.models_base import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "User"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    phone = Column(String(30), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    user_name = Column(String(30), nullable=False)
    time_account = Column(Integer())

    Service = relationship("Service", order_by="Service.id", back_populates="User", cascade="all")
    Serviceregister = relationship("Serviceregister", order_by="Serviceregister.id",
                                   back_populates="User", cascade="all")

    def __repr__(self):
        return f" User(id={self.id!r}, phone={self.phone!r}," \
               f" user_name={self.user_name!r}, time_account={self.time_account!r})"
