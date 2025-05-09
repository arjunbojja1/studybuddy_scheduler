from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from reactpy.backend.fastapi import configure
import json
import uvicorn

from exporter.file_exporter import FileExporter
from frontend.ui import StudyBuddyUI

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
configure(app, StudyBuddyUI)

# Create exporter
exporter = FileExporter()

@app.get("/download/{filetype}")
async def download_schedule(filetype: str, data: str):
    """API endpoint to download schedule data as either CSV or TXT.

    Args:
        filetype (str): Type of file to download (csv or txt).
        data (str): JSON string containing schedule data.
    """
    
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
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)