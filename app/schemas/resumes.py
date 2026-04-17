from pydantic import BaseModel,Field

class UploadResponse(BaseModel):
    id:int
    message:str
    original_filename:str
    saved_filename:str
    file_path:str
    file_type:str


class ResumeListItemResponse(BaseModel):
    id:int
    original_filename:str
    saved_filename:str
    file_path:str
    file_type:str


class ResumeDetailResponse(BaseModel):
    id:int
    original_filename:str
    saved_filename:str
    file_path:str
    file_type:str
    raw_text:str


class ResumeAnalysisResponse(BaseModel):
    """
    简历分析结果响应模型。
    用于返回对用户简历的结构化分析，包括总结、核心技能、优势、潜在风险以及改进建议。
    """
    summary:str = Field(description="总结简历")
    core_skills:list[str] = Field(description="用户的核心技能")
    strengths:list[str]  = Field(description="用户的优势")
    risks:list[str]   = Field(description="用户的风险挑战")
    suggestions:list[str] = Field(description="给用户的建议")