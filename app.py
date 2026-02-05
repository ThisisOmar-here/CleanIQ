"""
AI Storage Saver - Main Application
FastAPI server providing file scanning and AI analysis endpoints.
"""

import os
import subprocess
import platform
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from scanner import fast_scan, advance_scan, get_folder_sizes
from analyzer import get_available_models, analyze_file

app = FastAPI(
    title="AI Storage Saver",
    description="Smart file management with AI-powered analysis",
    version="1.0.0"
)

# Serve static files
static_path = Path(__file__).parent / "static"
static_path.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")


class SummarizeRequest(BaseModel):
    filepath: str
    model: str = "llama3.2"


@app.get("/")
async def root():
    """Serve the main HTML page."""
    index_path = static_path / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "AI Storage Saver API"}


@app.get("/api/models")
async def list_models():
    """Get available Ollama models."""
    models = get_available_models()
    return {"models": models}


@app.get("/api/scan")
async def scan_files(
    mode: str = Query("fast", description="Scan mode: 'fast' or 'advance'"),
    path: Optional[str] = Query(None, description="Path for advance scan"),
    exclude_system: bool = Query(False, description="Exclude system files")
):
    """
    Scan for large files.
    
    - **fast**: Scans common folders (Downloads, Desktop, Temp, etc.)
    - **advance**: Deep scan of all accessible drives or specified path
    """
    try:
        if mode == "fast":
            files = fast_scan(exclude_system=exclude_system)
            scan_path = "Common Folders (7 locations)"
        elif mode == "advance":
            if path:
                # User specified a path
                if not Path(path).exists():
                    raise HTTPException(status_code=400, detail="Invalid path")
                files = advance_scan(path, exclude_system=exclude_system)
                scan_path = path
            else:
                # Comprehensive scan of 35+ folders
                files = advance_scan(exclude_system=exclude_system)
                scan_path = "Comprehensive Scan (35+ locations)"
        else:
            raise HTTPException(status_code=400, detail="Invalid mode. Use 'fast' or 'advance'")
        
        # Count safe to delete files
        safe_count = sum(1 for f in files if f.get('safe_to_delete', False))
        
        return {
            "mode": mode,
            "path": scan_path,
            "file_count": len(files),
            "safe_count": safe_count,
            "files": files[:500],  # Return up to 500 files
            "total_size": sum(f['size_bytes'] for f in files),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/folders")
async def get_folders(path: Optional[str] = Query(None)):
    """Get folder sizes for visualization."""
    try:
        if not path:
            path = str(Path.home())
        folders = get_folder_sizes(path)
        return {"folders": folders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/summarize")
async def summarize_file(request: SummarizeRequest):
    """Generate AI summary for a file."""
    if not Path(request.filepath).exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    result = analyze_file(request.filepath, request.model)
    return result


@app.get("/api/open")
async def open_file(filepath: str = Query(..., description="Path to file to open")):
    """Open a file with the system default application."""
    try:
        path = Path(filepath)
        if not path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        # Platform-specific open command
        system = platform.system()
        if system == "Windows":
            os.startfile(str(path))
        elif system == "Darwin":  # macOS
            subprocess.run(["open", str(path)])
        else:  # Linux
            subprocess.run(["xdg-open", str(path)])
        
        return {"success": True, "message": f"Opened {path.name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/open-location")
async def open_file_location(filepath: str = Query(..., description="Path to file")):
    """Open the folder containing the file in file explorer."""
    try:
        path = Path(filepath)
        if not path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        folder = path.parent
        system = platform.system()
        if system == "Windows":
            # Select the file in Explorer
            subprocess.run(["explorer", "/select,", str(path)])
        elif system == "Darwin":  # macOS
            subprocess.run(["open", "-R", str(path)])
        else:  # Linux
            subprocess.run(["xdg-open", str(folder)])
        
        return {"success": True, "message": f"Opened folder containing {path.name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/delete")
async def delete_file(filepath: str = Query(..., description="Path to file to delete")):
    """Delete a file (moves to recycle bin on Windows)."""
    try:
        path = Path(filepath)
        if not path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        # For safety, we use send2trash if available, otherwise regular delete
        try:
            from send2trash import send2trash
            send2trash(str(path))
            return {"success": True, "message": f"Moved {path.name} to trash"}
        except ImportError:
            # Fallback: permanent delete (with warning)
            path.unlink()
            return {"success": True, "message": f"Deleted {path.name} permanently"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
