from fastapi import APIRouter,File,UploadFile
from app.schemas.resumes import *
from app.service.resumes_service import upload_resume,list_resumes,get_resume_detail,analyze_resume,get_resume_analysis



router = APIRouter(prefix="/resumes",tags=["resumes"])

@router.post("/upload",response_model=UploadResponse)
async def upload_file_api(file:UploadFile = File(...)):
    return await upload_resume(file)


@router.get("",response_model=list[ResumeListItemResponse])
def get_resumes_api():
    return list_resumes()


@router.get("/{resume_id}",response_model=ResumeDetailResponse)
def get_resume_detail_api(resume_id:int):
    return get_resume_detail(resume_id)


@router.post("/{resume_id}/analyze",response_model=ResumeAnalysisResponse)
def analyze_resume_api(resume_id:int):
    return analyze_resume(resume_id)


@router.get("/{resume_id}/analysis",response_model=ResumeAnalysisResponse)
def get_analysis_api(resume_id:int):
    return get_resume_analysis(resume_id)

