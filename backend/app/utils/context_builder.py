from typing import Optional
 
def build_context_from_inputs(
    title: str,
    business_model: str,
    project_type: str,
    # project_refers: str,
    summary: str,
    background: str,
    document_text: Optional[str] = None
) -> str:
    context = f"""
     Project Title: {title}
     Business Model: {business_model}
     Project Type: {project_type}
     Project Summary: {summary}
     Client Background: {background}
    """
 
    if document_text:
        context += f"\n Additional Document Info:\n{document_text[:]}"
 
    return context
