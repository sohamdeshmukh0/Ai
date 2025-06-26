from fastapi import APIRouter, BackgroundTasks, Form, UploadFile, File
from typing import Optional
from app.utils.context_builder import build_context_from_inputs
from rag.pipeline import Pipeline
from app.models import store_prompt_and_response_in_db
 
router = APIRouter(prefix="/projects", tags=["Project"])
import json
 
 
def clean_and_parse_response(response_str: str) -> dict:
    try:
        # Step 1: Remove escaped newlines and fix quote issues
        cleaned_str = response_str.replace('\n', '').replace('\\"', '"')
 
        # Step 2: Convert to dictionary
        parsed_json = json.loads(cleaned_str)
        return parsed_json
 
    except Exception as e:
        return {
            "error": "Failed to parse response",
            "details": str(e),
            "raw": response_str
        }
 
 
@router.post("/generate_questions")
async def generate_questions(
    background_tasks: BackgroundTasks,
    title: str = Form(...),
    business_model: str = Form(...),
    project_type: str = Form(...),
    # project_refers: str = Optional[UploadFile] = text(None),
    summary: str = Form(...),
    background: str = Form(...),
    uploaded_document: Optional[UploadFile] = File(None)
):
    document_text = ""
    if uploaded_document:
        document_text = (await uploaded_document.read()).decode("utf-8", errors="ignore")
 
    context = build_context_from_inputs(
        title,
        business_model,
        project_type,
        # project_refers,
        summary,
        background,
        document_text
    )
 
    pipeline = Pipeline()
 
    response = pipeline.process_prompt([context]).content
    response = clean_and_parse_response(response)
 
    background_tasks.add_task(
        store_prompt_and_response_in_db,
        context,
        response
    )
 
    return response
