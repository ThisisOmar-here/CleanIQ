"""
File Scanner Module
Scans directories to find large files and gather metadata.
Supports Fast Scan (common folders) and Advance Scan (full recursive).
"""

import os
import stat
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import concurrent.futures

# Common folders to prioritize in Fast Scan (7 folders)
FAST_SCAN_FOLDERS = [
    "Downloads",
    "Desktop",
    "Documents",
    "Videos",
    "Pictures",
    "Temp",
    "AppData\\Local\\Temp",
]

# Advanced Scan folders - comprehensive scan (35+ locations)
ADVANCE_SCAN_FOLDERS = [
    # All Fast Scan folders
    "Downloads", "Desktop", "Documents", "Videos", "Pictures",
    "Temp", "AppData\\Local\\Temp",
    
    # Additional user folders
    "Music",
    "OneDrive",
    "Dropbox",
    "Google Drive",
    "iCloud Drive",
    
    # AppData locations (common bloat)
    "AppData\\Local",
    "AppData\\Roaming",
    "AppData\\LocalLow",
    
    # Development folders
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
    
    # Game/App caches
    "Saved Games",
    "Games",
    ".minecraft",
    
    # Browser data
    "AppData\\Local\\Google\\Chrome\\User Data",
    "AppData\\Local\\Microsoft\\Edge\\User Data",
    "AppData\\Local\\Mozilla\\Firefox\\Profiles",
    "AppData\\Local\\BraveSoftware",
]

# System-wide paths to scan (non-user specific)
SYSTEM_SCAN_PATHS = [
    "C:\\Temp",
    "C:\\tmp",
    "C:\\Users\\Public",
]

# File extensions that can be summarized
SUMMARIZABLE_EXTENSIONS = {'.pdf', '.txt', '.docx', '.doc', '.xlsx', '.xls', '.csv'}

# Minimum file size to consider (10 MB)
MIN_SIZE_BYTES = 10 * 1024 * 1024

# System folders/patterns to exclude
SYSTEM_PATTERNS = {
    'Windows', 'Program Files', 'Program Files (x86)', 'ProgramData',
    '$Recycle.Bin', 'System Volume Information', 'Recovery',
    'AppData\\Local\\Microsoft', 'AppData\\Local\\Packages',
    'node_modules', '.git', '__pycache__', '.venv', 'venv',
}

# System file extensions to exclude
SYSTEM_EXTENSIONS = {
    '.dll', '.sys', '.exe', '.msi', '.cab',
    '.lnk', '.ini', '.dat', '.db', '.sqlite'
}

# Extensions that are SAFE TO DELETE (caches, temp, logs)
SAFE_EXTENSIONS = {
    '.log', '.tmp', '.temp', '.bak', '.old', '.cache',
    '.dmp', '.etl', '.crdownload', '.partial', '.chk',
    '.bac', '.~', '.swp', '.swo'
}

# Folder patterns that indicate SAFE TO DELETE content
SAFE_FOLDER_PATTERNS = {
    'cache', 'caches', 'temp', 'tmp', 'logs', 'log',
    'crash', 'crashdumps', 'backup', 'backups',
    'thumbnails', 'prefetch', 'shader', 'gpucache',
    'webcache', 'd3dscache', 'dxcache', 'localstorage',
    'codesignature', 'service worker'
}


def is_system_path(filepath: Path) -> bool:
    """Check if a path is a system path that should be excluded."""
    path_str = str(filepath)
    for pattern in SYSTEM_PATTERNS:
        if pattern in path_str:
            return True
    return False


def is_safe_to_delete(filepath: Path) -> bool:
    """
    Determine if a file is safe to delete (cache, temp, logs).
    Returns True for files that are unlikely to contain important user data.
    """
    path_str = str(filepath).lower()
    ext = filepath.suffix.lower()
    
    # Check extension
    if ext in SAFE_EXTENSIONS:
        return True
    
    # Check if path contains safe folder patterns
    for pattern in SAFE_FOLDER_PATTERNS:
        if pattern in path_str:
            return True
    
    return False


def is_system_file(filepath: Path) -> bool:
    """Check if a file is a system file based on extension."""
    return filepath.suffix.lower() in SYSTEM_EXTENSIONS


def get_file_info(filepath: Path, exclude_system: bool = False) -> Optional[Dict[str, Any]]:
    """Get detailed information about a file."""
    try:
        # Skip system files early if requested
        if exclude_system:
            if is_system_path(filepath) or is_system_file(filepath):
                return None
        
        stat_info = filepath.stat()
        size_bytes = stat_info.st_size
        
        # Skip small files
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
    """Convert bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def scan_directory(path: str, recursive: bool = True, exclude_system: bool = False, max_files: int = 500) -> List[Dict[str, Any]]:
    """
    Scan a directory for large files with improved performance using os.walk.
    
    Args:
        path: Directory path to scan
        recursive: If True, scan subdirectories recursively
        exclude_system: If True, skip system files and folders
        max_files: Maximum number of files to return
        
    Returns:
        List of file info dictionaries sorted by size (largest first)
    """
    files = []
    root_path = Path(path)
    files_checked = 0
    max_check = max_files * 10  # Check up to 10x to find large files
    
    if not root_path.exists():
        return []
    
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            # Skip system directories
            if exclude_system:
                dirnames[:] = [d for d in dirnames if d not in SYSTEM_PATTERNS and not any(p in dirpath for p in SYSTEM_PATTERNS)]
            
            # Limit recursion if not recursive mode
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
    
    # Sort by size (largest first) and limit
    files.sort(key=lambda x: x['size_bytes'], reverse=True)
    return files[:max_files]


def fast_scan(exclude_system: bool = False) -> List[Dict[str, Any]]:
    """
    Quick scan of common high-clutter folders.
    Targets Downloads, Desktop, Temp, etc.
    
    Returns:
        List of file info dictionaries sorted by size
    """
    files = []
    user_home = Path.home()
    
    for folder in FAST_SCAN_FOLDERS:
        folder_path = user_home / folder
        if folder_path.exists():
            files.extend(scan_directory(str(folder_path), recursive=True, exclude_system=exclude_system, max_files=100))
    
    # Also check Windows Temp
    temp_path = Path(os.environ.get('TEMP', ''))
    if temp_path.exists():
        files.extend(scan_directory(str(temp_path), recursive=False, exclude_system=exclude_system, max_files=50))
    
    # Remove duplicates and sort
    seen = set()
    unique_files = []
    for f in files:
        if f['path'] not in seen:
            seen.add(f['path'])
            unique_files.append(f)
    
    unique_files.sort(key=lambda x: x['size_bytes'], reverse=True)
    return unique_files[:200]


def advance_scan(path: Optional[str] = None, exclude_system: bool = False) -> List[Dict[str, Any]]:
    """
    Comprehensive scan of many directories.
    If path is provided, scans that path.
    If no path, scans 35+ common folders where large files accumulate.
    
    Args:
        path: Optional specific directory to scan
        exclude_system: If True, skip system files and folders
        
    Returns:
        List of file info dictionaries sorted by size
    """
    if path:
        # User specified a path - scan just that
        return scan_directory(path, recursive=True, exclude_system=exclude_system, max_files=500)
    
    # No path specified - comprehensive scan of all advanced folders
    files = []
    user_home = Path.home()
    
    # Scan all user folders from ADVANCE_SCAN_FOLDERS
    for folder in ADVANCE_SCAN_FOLDERS:
        folder_path = user_home / folder
        if folder_path.exists():
            try:
                files.extend(scan_directory(str(folder_path), recursive=True, exclude_system=True, max_files=100))
            except (PermissionError, OSError):
                continue
    
    # Scan system-wide paths
    for sys_path in SYSTEM_SCAN_PATHS:
        if Path(sys_path).exists():
            try:
                files.extend(scan_directory(sys_path, recursive=True, exclude_system=True, max_files=50))
            except (PermissionError, OSError):
                continue
    
    # Also check Windows Temp
    temp_path = Path(os.environ.get('TEMP', ''))
    if temp_path.exists():
        files.extend(scan_directory(str(temp_path), recursive=True, exclude_system=True, max_files=100))
    
    # Remove duplicates and sort by size
    seen = set()
    unique_files = []
    for f in files:
        if f['path'] not in seen:
            seen.add(f['path'])
            unique_files.append(f)
    
    unique_files.sort(key=lambda x: x['size_bytes'], reverse=True)
    return unique_files[:500]  # Return top 500 largest files


def get_folder_sizes(path: str, max_depth: int = 2) -> List[Dict[str, Any]]:
    """
    Get sizes of immediate subfolders for visualization.
    
    Args:
        path: Root directory
        max_depth: How deep to calculate sizes
        
    Returns:
        List of folder info dictionaries
    """
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
