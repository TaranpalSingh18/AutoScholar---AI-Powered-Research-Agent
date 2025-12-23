"""
Main API Server
FastAPI server for Research Agent workflow
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional
from src.workflow import ResearchWorkflow
import uvicorn
import config

app = FastAPI(title="Research Agent API", version="1.0.0")


class ResearchRequest(BaseModel):
    """Request model for research generation"""
    topic: str
    description: str
    methodology_input: Optional[str] = None


class ResearchResponse(BaseModel):
    """Response model for research generation"""
    success: bool
    topic: str
    abstract: str
    introduction: str
    literature_review: str
    methodology: str
    references: str
    latex: Optional[str] = None
    flowchart_url: Optional[str] = None
    github_url: Optional[str] = None
    error: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Research Agent API",
        "version": "1.0.0",
        "endpoints": {
            "/research": "POST - Generate research paper",
            "/health": "GET - Health check"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/research", response_model=ResearchResponse)
async def generate_research(request: ResearchRequest):
    """
    Generate research paper
    
    This endpoint replicates the n8n workflow:
    1. Fetches papers from arXiv
    2. Generates abstract, introduction, literature review
    3. Creates references and citations
    4. Generates methodology
    5. Creates LaTeX document
    6. Uploads to GitHub
    """
    try:
        workflow = ResearchWorkflow()
        result = workflow.execute(
            topic=request.topic,
            description=request.description,
            methodology_input=request.methodology_input
        )
        
        return ResearchResponse(
            success=result.get("success", False),
            topic=result.get("topic", ""),
            abstract=result.get("abstract", ""),
            introduction=result.get("introduction", ""),
            literature_review=result.get("literature_review", ""),
            methodology=result.get("methodology", ""),
            references=result.get("references", ""),
            latex=result.get("latex"),
            flowchart_url=result.get("flowchart_url"),
            github_url=result.get("github_url"),
            error=result.get("error")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/research/form")
async def research_form(topic: str, description: str):
    """
    Form submission endpoint (matches n8n form trigger)
    
    This endpoint accepts form data and triggers the research workflow
    """
    try:
        workflow = ResearchWorkflow()
        result = workflow.execute(
            topic=topic,
            description=description
        )
        
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=True
    )

