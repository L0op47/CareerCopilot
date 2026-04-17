from app.db.base import Base
from sqlalchemy import Column,Integer,String


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer,primary_key=True,index=True)
    original_filename = Column(String)
    saved_filename = Column(String)
    file_path = Column(String)
    file_type = Column(String)
    raw_text = Column(String)
