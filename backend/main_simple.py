from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import uuid
import os
from typing import Dict, Any

from backend.services.orchestrator import Orchestrator
from backend.services.file_processor import FileProcessor

app = FastAPI(
    title="RFP Agentic AI System",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="backend/templates")

processing_results = {}
file_processor = FileProcessor()
orchestrator = Orchestrator()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return templates.TemplateResponse("index.html", {"request": {}})

@app.post("/api/v1/upload-rfp")
async def upload_rfp(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    try:
        if not file.filename:
            raise HTTPException(400, "No file provided")
        
        allowed_extensions = ['.pdf', '.doc', '.docx', '.txt']
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(400, f"Unsupported file type. Allowed: {allowed_extensions}")
        
        file_path = await file_processor.save_uploaded_file(file)
        request_id = str(uuid.uuid4())
        
        processing_results[request_id] = {"status": "processing", "file_path": file_path}
        
        background_tasks.add_task(process_rfp_background, request_id, file_path)
        
        return {
            "request_id": request_id,
            "status": "processing",
            "message": "RFP uploaded and processing started",
            "filename": file.filename
        }
        
    except Exception as e:
        raise HTTPException(500, f"Upload failed: {str(e)}")

@app.get("/api/v1/quotation/{request_id}")
async def get_quotation(request_id: str):
    if request_id not in processing_results:
        raise HTTPException(404, "Request not found")
    
    result = processing_results[request_id]
    
    if result["status"] == "processing":
        raise HTTPException(425, "Processing not completed yet")
    
    if result["status"] == "error":
        raise HTTPException(500, f"Processing failed: {result.get('message', 'Unknown error')}")
    
    return {
        "request_id": request_id,
        "status": "completed",
        "quotation": result["quotation"]
    }

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "RFP Agentic AI System",
        "version": "2.0.0"
    }

async def process_rfp_background(request_id: str, file_path: str):
    try:
        result = await orchestrator.process_rfp(file_path)
        processing_results[request_id] = result
    except Exception as e:
        processing_results[request_id] = {
            "status": "error", 
            "message": str(e)
        }

if __name__ == "__main__":
    uvicorn.run("backend.main_simple:app", host="0.0.0.0", port=8000, reload=True)
