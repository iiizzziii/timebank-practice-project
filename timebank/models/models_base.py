import enum
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ServiceregisterStatusEnum(enum.Enum):
    inprogress = 1
    ended = 2
