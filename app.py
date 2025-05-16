from fastapi import FastAPI, Request
from fastapi.responses import Response, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from reactpy.backend.fastapi import configure, Options
import json
import uvicorn

from exporter.file_exporter import FileExporter
from frontend.ui import StudyBuddyUI

"""Main application script for the StudyBuddy Scheduler.

This script sets up a FastAPI application with ReactPy for the frontend
and provides endpoints for downloading schedules in CSV or text format.
"""

# Create FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure ReactPy
configure(app, StudyBuddyUI, options=Options(url_prefix="/app"))

# Create exporter
exporter = FileExporter()

@app.get("/download/{filetype}")
async def download_schedule(filetype: str, data: str):
    """Endpoint to download the schedule in the specified file format.

    Args:
        filetype (str): The file format ('csv' or 'txt').
        data (str): The schedule data in JSON format.

    Returns:
        Response: A file response with the schedule in the requested format.
    """
    if not data:
        return Response("No data provided", status_code=400)

    try:
        # Parse JSON data
        schedule = json.loads(data)
    except json.JSONDecodeError:
        return Response("Invalid JSON data", status_code=400)
    
    if filetype == "csv":
        content = exporter.export_to_csv(schedule)
        return Response(
            content,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=schedule.csv"},
        )
    elif filetype == "txt":
        content = exporter.export_to_txt(schedule)
        return Response(
            content,
            media_type="text/plain",
            headers={"Content-Disposition": "attachment; filename=schedule.txt"},
        )
    else:
        return Response("Invalid file type", status_code=400)
    
@app.get("/")
async def root():
    """Redirects the root URL to the ReactPy application."""
    return RedirectResponse(url="/app")
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)