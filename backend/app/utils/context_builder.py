from typing import Optional

def build_context_from_inputs(
    project_title: str,
    business_model: str,
    project_type: str,
    references: str,
    project_summary: str,
    client_background: str,
    document_text: Optional[str] = None
) -> str:
    context = f"""
     Project Title: {project_title}
     Business Model: {business_model}
     Project Type: {project_type}
     References: {references}
     Project Summary: {project_summary}
     Client Background: {client_background}
    """

    if document_text:
        context += f"\n Additional Document Info:\n{document_text[:]}"

    return context
