from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey

from db.base_class import Base 
from db.models.cluster import Cluster


class Records(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=False)
    upload_date = Column(DateTime,default=datetime.utcnow)
    vector_processed = Column(Boolean, default=False)
    embedding_model = Column(String, nullable=True)
    cluster_id = Column(Integer, ForeignKey(Cluster.id), nullable=True)
    
