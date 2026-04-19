from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from app.models import ReviewRequest, ReviewResponse
from app.services.orchestrator import ReviewOrchestrator
from app.services.report_service import ReportService

# Load environment variables
load_dotenv()

app = FastAPI(title="Code Review Agent API", version="1.0.0")

# Initialize orchestrator
orchestrator = ReviewOrchestrator()
report_service = ReportService()

@app.post("/review", response_model=ReviewResponse)
async def review_code(request: ReviewRequest):
    try:
        review_result = await orchestrator.review(request.code, request.language)
        return review_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/review/report")
async def generate_report(request: ReviewRequest, format: str = Query("txt", regex="^(txt|pdf)$")):
    try:
        review_result = await orchestrator.review(request.code, request.language)
        report_path = report_service.generate_report(review_result, format)
        
        if format == "txt":
            # For TXT, report_service returns the content string, not path. Wait, let's check report_service.
            # Ah, report_service.generate_report returns string for TXT and path for PDF.
            # We should probably standardize. Let's fix report_service or handle it here.
            # Let's handle it here.
            pass 
            
        # Actually, let's look at report_service again.
        # _generate_txt returns string. _generate_pdf returns path.
        # This is inconsistent. I should fix report_service to always return a path or always return content.
        # For file download, path is better.
        
        # Let's modify this block to handle the inconsistency for now, or better, fix report_service.
        # I'll fix report_service in the next step if needed, but for now let's write to a temp file for TXT too.
        
        if format == "txt":
             import tempfile
             with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".txt") as tmp:
                 tmp.write(report_service.generate_report(review_result, "txt"))
                 report_path = tmp.name
        else:
             report_path = report_service.generate_report(review_result, "pdf")

        return FileResponse(report_path, filename=f"review_report.{format}", media_type="application/octet-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
