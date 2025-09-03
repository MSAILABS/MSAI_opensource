from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from db.base_class import Base 


class Cluster(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    created_date = Column(DateTime,default=datetime.utcnow)

