from timebank.models.models_base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Service(Base):
    __tablename__ = "Service"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    title = Column(String(1000), nullable=False)
    user_id = Column(Integer(), ForeignKey('User.id'), nullable=False)
    estimate = Column(Integer())
    avg_rating = Column(Integer())

    User = relationship("User", order_by="User.id", back_populates="Service", cascade="all")
    Serviceregister = relationship("Serviceregister", order_by="Serviceregister.id",
                                   back_populates="Service", cascade="all")

    def __repr__(self):
        return f" Service(id={self.id!r}, title={self.title!r}, user_id={self.user_id!r}" \
               f", estimate={self.estimate!r}, avg_rating={self.avg_rating!r})"
