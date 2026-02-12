import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

FAST_SCAN_FOLDERS = [
    "Downloads",
    "Desktop",
    "Documents",
    "Videos",
    "Pictures",
    "Temp",
    "AppData\\Local\\Temp",
]

ADVANCE_SCAN_FOLDERS = [
    "Downloads", "Desktop", "Documents", "Videos", "Pictures",
    "Temp", "AppData\\Local\\Temp",
    
    "Music",
    "OneDrive",
    "Dropbox",
    "Google Drive",
    "iCloud Drive",
    
    "AppData\\Local",
    "AppData\\Roaming",
    "AppData\\LocalLow",
    
    ".vscode",
    ".npm",
    ".nuget",
    ".gradle",
    ".m2",
    ".docker",
    ".cache",
    ".composer",
    ".cargo",
    ".rustup",
    
    "Saved Games",
    "Games",
    ".minecraft",
    
    "AppData\\Local\\Google\\Chrome\\User Data",
    "AppData\\Local\\Microsoft\\Edge\\User Data",
    "AppData\\Local\\Mozilla\\Firefox\\Profiles",
    "AppData\\Local\\BraveSoftware",
]

SYSTEM_SCAN_PATHS = [
    "C:\\Temp",
    "C:\\tmp",
    "C:\\Users\\Public",
]

SUMMARIZABLE_EXTENSIONS = {'.pdf', '.txt', '.docx', '.doc', '.xlsx', '.xls', '.csv'}

MIN_SIZE_BYTES = 10 * 1024 * 1024

SYSTEM_PATTERNS = {
    'Windows', 'Program Files', 'Program Files (x86)', 'ProgramData',
    '$Recycle.Bin', 'System Volume Information', 'Recovery',
    'AppData\\Local\\Microsoft', 'AppData\\Local\\Packages',
    'node_modules', '.git', '__pycache__', '.venv', 'venv',
}

SYSTEM_EXTENSIONS = {
    '.dll', '.sys', '.exe', '.msi', '.cab',
    '.lnk', '.ini', '.dat', '.db', '.sqlite'
}

SAFE_EXTENSIONS = {
    '.log', '.tmp', '.temp', '.bak', '.old', '.cache',
    '.dmp', '.etl', '.crdownload', '.partial', '.chk',
    '.bac', '.~', '.swp', '.swo'
}

SAFE_FOLDER_PATTERNS = {
    'cache', 'caches', 'temp', 'tmp', 'logs', 'log',
    'crash', 'crashdumps', 'backup', 'backups',
    'thumbnails', 'prefetch', 'shader', 'gpucache',
    'webcache', 'd3dscache', 'dxcache', 'localstorage',
    'codesignature', 'service worker'
}


def is_system_path(filepath: Path) -> bool:
    path_str = str(filepath)
    for pattern in SYSTEM_PATTERNS:
        if pattern in path_str:
            return True
    return False


def is_safe_to_delete(filepath: Path) -> bool:
    path_str = str(filepath).lower()
    ext = filepath.suffix.lower()
    
    if ext in SAFE_EXTENSIONS:
        return True
    
    for pattern in SAFE_FOLDER_PATTERNS:
        if pattern in path_str:
            return True
    
    return False


def is_system_file(filepath: Path) -> bool:
    return filepath.suffix.lower() in SYSTEM_EXTENSIONS


def get_file_info(filepath: Path, exclude_system: bool = False) -> Optional[Dict[str, Any]]:
    try:
        if exclude_system:
            if is_system_path(filepath) or is_system_file(filepath):
                return None
        
        stat_info = filepath.stat()
        size_bytes = stat_info.st_size
        
        if size_bytes < MIN_SIZE_BYTES:
            return None
            
        extension = filepath.suffix.lower()
        
        return {
            "path": str(filepath),
            "name": filepath.name,
            "extension": extension,
            "size_bytes": size_bytes,
            "size_readable": format_size(size_bytes),
            "modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
            "accessed": datetime.fromtimestamp(stat_info.st_atime).isoformat(),
            "can_summarize": extension in SUMMARIZABLE_EXTENSIONS,
            "safe_to_delete": is_safe_to_delete(filepath),
        }
    except (PermissionError, OSError, FileNotFoundError):
        return None


def format_size(size_bytes: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def scan_directory(path: str, recursive: bool = True, exclude_system: bool = False, max_files: int = 500):
    files = []
    root_path = Path(path)
    files_checked = 0
    max_check = max_files * 10  # Check up to 10x to find large files
    
    if not root_path.exists():
        return []
    
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            if exclude_system:
                dirnames[:] = [d for d in dirnames if d not in SYSTEM_PATTERNS and not any(p in dirpath for p in SYSTEM_PATTERNS)]
            
            if not recursive:
                dirnames.clear()
            
            for filename in filenames:
                if files_checked >= max_check:
                    break
                    
                files_checked += 1
                filepath = Path(dirpath) / filename
                
                try:
                    file_info = get_file_info(filepath, exclude_system)
                    if file_info:
                        files.append(file_info)
                except (PermissionError, OSError):
                    continue
            
            if files_checked >= max_check:
                break
                
    except (PermissionError, OSError):
        pass
    
    files.sort(key=lambda x: x['size_bytes'], reverse=True)
    return files[:max_files]


def fast_scan(exclude_system: bool = False):
    files = []
    user_home = Path.home()
    
    for folder in FAST_SCAN_FOLDERS:
        folder_path = user_home / folder
        if folder_path.exists():
            files.extend(scan_directory(str(folder_path), recursive=True, exclude_system=exclude_system, max_files=100))
    
    temp_path = Path(os.environ.get('TEMP', ''))
    if temp_path.exists():
        files.extend(scan_directory(str(temp_path), recursive=False, exclude_system=exclude_system, max_files=50))
    
    seen = set()
    unique_files = []
    for f in files:
        if f['path'] not in seen:
            seen.add(f['path'])
            unique_files.append(f)
    
    unique_files.sort(key=lambda x: x['size_bytes'], reverse=True)
    return unique_files[:200]


def advance_scan(path: Optional[str] = None, exclude_system: bool = False):
    if path:
        return scan_directory(path, recursive=True, exclude_system=exclude_system, max_files=500)
    
    files = []
    user_home = Path.home()
    
    for folder in ADVANCE_SCAN_FOLDERS:
        folder_path = user_home / folder
        if folder_path.exists():
            try:
                files.extend(scan_directory(str(folder_path), recursive=True, exclude_system=True, max_files=100))
            except (PermissionError, OSError):
                continue
    
    for sys_path in SYSTEM_SCAN_PATHS:
        if Path(sys_path).exists():
            try:
                files.extend(scan_directory(sys_path, recursive=True, exclude_system=True, max_files=50))
            except (PermissionError, OSError):
                continue
    
    temp_path = Path(os.environ.get('TEMP', ''))
    if temp_path.exists():
        files.extend(scan_directory(str(temp_path), recursive=True, exclude_system=True, max_files=100))
    
    seen = set()
    unique_files = []
    for f in files:
        if f['path'] not in seen:
            seen.add(f['path'])
            unique_files.append(f)
    
    unique_files.sort(key=lambda x: x['size_bytes'], reverse=True)
    return unique_files[:500]


def get_folder_sizes(path: str):
    folders = []
    root_path = Path(path)
    
    if not root_path.exists():
        return []
    
    try:
        for item in root_path.iterdir():
            if item.is_dir():
                total_size = 0
                file_count = 0
                try:
                    for f in item.rglob('*'):
                        if f.is_file():
                            try:
                                total_size += f.stat().st_size
                                file_count += 1
                            except (PermissionError, OSError):
                                pass
                except (PermissionError, OSError):
                    pass
                
                if total_size > 0:
                    folders.append({
                        "path": str(item),
                        "name": item.name,
                        "size_bytes": total_size,
                        "size_readable": format_size(total_size),
                        "file_count": file_count,
                    })
    except (PermissionError, OSError):
        pass
    
    folders.sort(key=lambda x: x['size_bytes'], reverse=True)
    return folders
