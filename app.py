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

app = FastAPI()

static_path = Path(__file__).parent / "static"
static_path.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")


class SummarizeRequest(BaseModel):
    filepath: str
    model: str = "llama3.2"


@app.get("/")
async def root():
    index_path = static_path / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "AI Storage Saver API"}


@app.get("/api/models")
async def list_models():
    models = get_available_models()
    return {"models": models}


@app.get("/api/scan")
async def scan_files(
    mode: str = Query("fast"),
    path: Optional[str] = Query(None),
    exclude_system: bool = Query(False)
):
    try:
        if mode == "fast":
            files = fast_scan(exclude_system=exclude_system)
            scan_path = "Common Folders (7 locations)"
        elif mode == "advance":
            if path:
                if not Path(path).exists():
                    raise HTTPException(status_code=400, detail="Invalid path")
                files = advance_scan(path, exclude_system=exclude_system)
                scan_path = path
            else:
                files = advance_scan(exclude_system=exclude_system)
                scan_path = "Comprehensive Scan (35+ locations)"
        else:
            raise HTTPException(status_code=400, detail="Invalid mode. Use 'fast' or 'advance'")
        
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
    try:
        if not path:
            path = str(Path.home())
        folders = get_folder_sizes(path)
        return {"folders": folders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/summarize")
async def summarize_file(request: SummarizeRequest):
    if not Path(request.filepath).exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    result = analyze_file(request.filepath, request.model)
    return result


@app.get("/api/open")
async def open_file(filepath: str = Query(...)):
    try:
        path = Path(filepath)
        if not path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        system = platform.system()
        if system == "Windows":
            os.startfile(str(path))
        elif system == "Darwin":
            subprocess.run(["open", str(path)])
        else:
            subprocess.run(["xdg-open", str(path)])
        
        return {"success": True, "message": f"Opened {path.name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/open-location")
async def open_file_location(filepath: str = Query(...)):
    try:
        path = Path(filepath)
        if not path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        folder = path.parent
        system = platform.system()
        if system == "Windows":
            subprocess.run(["explorer", "/select,", str(path)])
        elif system == "Darwin":
            subprocess.run(["open", "-R", str(path)])
        else:
            subprocess.run(["xdg-open", str(folder)])
        
        return {"success": True, "message": f"Opened folder containing {path.name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/delete")
async def delete_file(filepath: str = Query(...)):
    try:
        path = Path(filepath)
        if not path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        try:
            from send2trash import send2trash
            send2trash(str(path))
            return {"success": True, "message": f"Moved {path.name} to trash"}
        except ImportError:
            path.unlink()
            return {"success": True, "message": f"Deleted {path.name} permanently"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
