import uuid

from fastapi import UploadFile,HTTPException
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader,Docx2txtLoader

from app.schemas.resumes import UploadResponse,ResumeListItemResponse,ResumeDetailResponse
from app.core.settings import RAW_DATA_DIR
from app.db.session import SessionLocal
from app.models.resume import Resume
import app.service.llm_service as llm


allowed_suffixes  = {".pdf",".txt",".docx"}

def _validate_suffix(filename:str) -> str:
    suffix  = Path(filename).suffix.lower()
    if suffix not in allowed_suffixes:
        raise HTTPException(status_code=400,detail="不支持上传的文件类型")
    return suffix


async def _save_file(file:UploadFile,saved_path:Path):
    content = await file.read()
    saved_path.write_bytes(content)


def _load_resume_content(file_path:Path,suffix:str) -> str:
    if suffix == ".pdf":
        loader = PyPDFLoader(str(file_path))
        docs = loader.load()
        return "\n".join(doc.page_content for doc in docs)

    if suffix == ".docx":
        loader=Docx2txtLoader(str(file_path))
        docs = loader.load()
        return "\n".join(doc.page_content for doc in docs)
    
    if suffix == ".txt":
        docs = file_path.read_text(encoding="utf-8")
        return docs

    raise HTTPException(status_code=400,detail="暂不支持该文件类型")


async def upload_resume(file:UploadFile)->UploadResponse:

    if not file.filename:
        raise HTTPException(status_code=400,detail="文件名不可为空")
    suffix = _validate_suffix(file.filename)
    saved_name = str(uuid.uuid4()) + suffix
    saved_path = RAW_DATA_DIR / saved_name
    
    await _save_file(file,saved_path)
    
    raw_text = _load_resume_content(saved_path,suffix)

    db = SessionLocal()
    try:
        resume = Resume(
            original_filename = file.filename,
            saved_filename = saved_name,
            file_path = str(saved_path),
            file_type = suffix,
            raw_text = raw_text
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)
    finally:
        db.close()
    return UploadResponse(
        message="上传成功",
        id = resume.id,
        original_filename=file.filename,
        saved_filename = saved_name,
        file_path=str(saved_path),
        file_type=suffix
    )


def list_resumes()-> ResumeListItemResponse:
    db = SessionLocal()
    try:
        resumes = db.query(Resume).all()
        return[
            ResumeListItemResponse(
                id=resume.id,
                original_filename=resume.original_filename,
                saved_filename=resume.saved_filename,
                file_path=resume.file_path,
                file_type=resume.file_type,
            )
            for resume in resumes
        ]
    finally:
        db.close()


def get_resume_detail(resume_id:int)->ResumeDetailResponse:
    db = SessionLocal()
    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            raise HTTPException(status_code=404,detail="简历不存在")
        return ResumeDetailResponse(
                id=resume.id,
                original_filename=resume.original_filename,
                saved_filename=resume.saved_filename,
                file_path=resume.file_path,
                file_type=resume.file_type,
                raw_text = resume.raw_text
            )
    finally:
        db.close()


def analyze_resume(resume_id:int):
    resume = get_resume_detail(resume_id)
    return llm.run(resume.raw_text)

