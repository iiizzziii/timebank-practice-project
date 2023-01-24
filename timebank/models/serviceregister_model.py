from timebank.models.models_base import Base, ServiceregisterStatusEnum
from sqlalchemy import Column, Integer, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship


class Serviceregister(Base):
    __tablename__ = "Serviceregister"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    service_id = Column(Integer(), ForeignKey('Service.id'), nullable=False)
    consumer_id = Column(Integer(), ForeignKey('User.id'), nullable=False)
    hours = Column(Integer())
    service_status = Column(Enum(ServiceregisterStatusEnum), nullable=False)
    end_time = Column(Date())
    rating = Column(Integer())

    User = relationship("User", order_by="User.id", back_populates="Serviceregister", cascade="all")
    Service = relationship("Service", order_by="Service.id", back_populates="Serviceregister", cascade="all")

    def __repr__(self):
        return f" Serviceregister(id={self.id!r}, service_id={self.service_id!r}, service_id={self.service_id!r}," \
               f" consumer_id={self.consumer_id!r}, hours={self.hours!r},  service_status={self.service_status!r}," \
               f" end_time={self.end_time!r})"
