from fastapi import FastAPI
from pydantic import BaseModel
from .qa_engine import TechDebtQnA
from .metrics_parser import extract_metrics
from .metrics_parser import extract_raw_text_lines

app = FastAPI()
qa_engine = TechDebtQnA()
metrics_cache = extract_metrics()

extract_raw_text_lines()


class QueryRequest(BaseModel):
    question: str

@app.post("/ask_tech_debt")
def ask_tech_debt(req: QueryRequest):
    answer = qa_engine.answer_question(req.question)
    return {"answer": answer}


@app.get("/metrics_summary/{project_name}")
def get_project_metrics(project_name: str):
    search = project_name.strip().lower()

    for stored_project in metrics_cache:
        if stored_project.lower() == search:
            return {stored_project: metrics_cache[stored_project]}

    return {"error": f"No metrics found for project '{project_name}'"}

@app.get("/project_names")
def list_project_names():
    return {"projects": list(metrics_cache.keys())}


















# from fastapi import FastAPI
# from pydantic import BaseModel
# from app.qa_engine import TechDebtQnA

# app = FastAPI()
# qa_engine = TechDebtQnA()

# class QueryRequest(BaseModel):
#     question: str

# @app.post("/ask_tech_debt")
# def ask_tech_debt(req: QueryRequest):
#     return {"answer": qa_engine.answer_question(req.question)}
