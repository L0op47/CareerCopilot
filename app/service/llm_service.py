from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.schemas.resumes import ResumeAnalysisResponse
 
from app.core.settings import API_KEY,BASE_URL,MODEL
llm = ChatOpenAI(
    model=MODEL,
    api_key=API_KEY,
    base_url=BASE_URL,
    temperature=0,
)

prompt = ChatPromptTemplate.from_messages([
    ("system","你是一个职场高手，你的任务是分析用户发来的简历，对用户的简历进行总结，提取出用户的核心技能，长处，给出相应的建议，你必须返回 JSON，按给定字段输出，不要输出 JSON 以外的内容，输出字段必须包含：summary,core_skills,strengths,risks,suggestions,不要输出额外解释"),
    ("human","{raw_text}"),
])

def run(raw_text:str):
    chain = prompt | llm.with_structured_output(ResumeAnalysisResponse)
    result = chain.invoke({"raw_text":raw_text})
    return result