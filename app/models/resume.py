from app.db.base import Base
from sqlalchemy import Column, ForeignKey,Integer,String
from sqlalchemy.orm import foreign, relationship


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer,primary_key=True,index=True)
    original_filename = Column(String)
    saved_filename = Column(String)
    file_path = Column(String)
    file_type = Column(String)
    raw_text = Column(String)
    file_hash = Column(String,unique=True,index=True)

    analysis = relationship(
        "ResumeAnalysis",
        back_populates="resume",
        uselist=False,
        cascade="all,delete-orphan"
    )

class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"
    id = Column(Integer,primary_key=True,index=True)
    resume_id = Column(Integer,ForeignKey("resumes.id"),index=True,unique=True)
    summary = Column(String)
    core_skills = Column(String)
    strengths = Column(String)
    risks = Column(String)
    suggestions = Column(String)
    status = Column(String,default="done")

    resume = relationship(
        "Resume",
        back_populates="analysis"
    )
