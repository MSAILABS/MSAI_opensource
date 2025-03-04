from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from db.base_class import Base 


class Records(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=False)
    upload_date = Column(DateTime,default=datetime.utcnow)
    
