<p align="center">
  <img src="static/logo.png" alt="CleanIQ Logo" width="150" height="150">
</p>

<h1 align="center">CleanIQ</h1>

<p align="center">
  <strong>Your intelligent, privacy-first storage assistant powered by local AI.</strong>
</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+"></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-0.109-009688.svg" alt="FastAPI"></a>
  <a href="https://ollama.com"><img src="https://img.shields.io/badge/Ollama-Powered-blueviolet.svg" alt="Ollama"></a>
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
</p>

<p align="center">
  <a href="#-features"><img src="https://img.shields.io/badge/-Features-00bfff" alt="Features"></a>
  <a href="#-how-it-works"><img src="https://img.shields.io/badge/-How_It_Works-ff6b6b" alt="How It Works"></a>
  <a href="#-installation"><img src="https://img.shields.io/badge/-Installation-34c759" alt="Installation"></a>
  <a href="#-api-reference"><img src="https://img.shields.io/badge/-API_Reference-af52de" alt="API"></a>
  <a href="#-contributing"><img src="https://img.shields.io/badge/-Contributing-ff9500" alt="Contributing"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/ThisisOmar-here/cleaniq?style=social" alt="GitHub Stars">
  <img src="https://img.shields.io/github/forks/ThisisOmar-here/cleaniq?style=social" alt="GitHub Forks">
  <img src="https://img.shields.io/github/issues/ThisisOmar-here/cleaniq" alt="GitHub Issues">
  <img src="https://img.shields.io/github/last-commit/ThisisOmar-here/cleaniq" alt="Last Commit">
</p>

---

## 📖 Overview

**CleanIQ** is a **Smart Storage Saver** designed to help you regain control over your digital clutter. It's not just about finding large files—it's about identifying the files you haven't touched in years.

Unlike traditional disk cleaners, CleanIQ uses **local Artificial Intelligence** to analyze your files and highlights content that has been **modified or accessed a long time ago**. It helps you distinguish between "important archives" and "forgotten junk" without your data ever leaving your computer.

### 🔐 Privacy First

All AI processing happens **100% locally** on your machine using [Ollama](https://ollama.com). Your files are **never uploaded** to any external server. Your data stays yours.

---

## ✨ Features

### 🧠 Smart Age Detection
CleanIQ specifically targets files that are taking up space **and** haven't been needed for a long time.
- **Find Forgotten Files**: Instantly see files you haven't opened in years.
- **Access Time Analysis**: Sorts files not just by size, but by when they were last accessed.
- **Intelligent Cleanup**: Helps you safely remove old logs, caches, and downloads that have been sitting gathering dust.

### 🔍 Smart Scanning Modes

| Mode | Locations | Use Case |
|:-----|:----------|:---------|
| **⚡ Fast Scan** | 7 common folders | Quick cleanup of recent clutter |
| **🛡️ Advanced Scan** | 35+ locations | Deep analysis of long-forgotten files |

#### Fast Scan Targets
- Downloads
- Desktop  
- Documents
- Videos
- Pictures
- Temp folders
- AppData\Local\Temp

#### Advanced Scan Coverage
<details>
<summary><strong>📂 Click to expand full list (35+ locations)</strong></summary>

**User Folders:**
- Downloads, Desktop, Documents, Videos, Pictures, Music
- OneDrive, Dropbox, Google Drive, iCloud Drive

**AppData Locations:**
- AppData\Local
- AppData\Roaming
- AppData\LocalLow

**Development Caches:**
- `.vscode`, `.npm`, `.nuget`, `.gradle`, `.m2`
- `.docker`, `.cache`, `.composer`, `.cargo`, `.rustup`

**Gaming & Applications:**
- Saved Games, Games, .minecraft

**Browser Data:**
- Chrome User Data
- Edge User Data
- Firefox Profiles
- Brave Browser Data

**System Locations:**
- C:\Temp, C:\tmp
- C:\Users\Public
- Windows Temp directories

</details>

---

### 🤖 AI-Powered File Analysis

CleanIQ doesn't just show you file names—it tells you **what's inside**.

| Feature | Description |
|:--------|:------------|
| **📝 Instant Summaries** | Click "Analyze with AI" to get a concise 1-sentence summary of any document |
| **⚠️ Importance Rating** | Files are classified as High, Medium, or Low importance |
| **💡 Smart Recommendations** | Get actionable advice: "Keep", "Review", or "Safe to delete" |
| **📄 Supported Formats** | PDF, Word (.docx/.doc), Excel (.xlsx/.xls), Text (.txt), CSV |

**Example AI Analysis:**
> *"This is an old receipt from Amazon dated 2022. You haven't opened it since then. **Low importance** — Safe to delete."*

---

### 🛡️ Safe-to-Delete Detection

CleanIQ automatically identifies files that are typically safe to remove:

**Safe Extensions:**
`.log` `.tmp` `.temp` `.bak` `.old` `.cache` `.dmp` `.etl` `.crdownload` `.partial` `.chk` `.swp`

**Safe Folder Patterns:**
`cache` `caches` `temp` `tmp` `logs` `crash` `crashdumps` `thumbnails` `prefetch` `shader` `gpucache` `webcache`

Files are tagged with visual badges:
- ✅ **Safe** — Cache, temp, and log files safe to delete
- ⚠️ **Review** — Documents, media, or code that need your attention

---

### 🎨 Beautiful, Modern UI

- **Apple-Inspired Design** — Clean, minimal interface with glassmorphism sidebar
- **Interactive File Cards** — Color-coded icons by file type (PDF, Document, Excel, Image, Video, Archive)
- **Smooth Animations** — Hover effects and real-time scanning updates
- **Smart Sorting** — Sort by Size, Name, or **Date Modified/Accessed**
- **Safe Filter Toggle** — Instantly show only files safe to delete

---

### ⚡ Powerful File Management

| Action | Description |
|:-------|:------------|
| **🔓 Open File** | Launch file with default system application |
| **📂 Open Location** | Jump to file's folder in Explorer/Finder |
| **🗑️ Safe Delete** | Move files to Recycle Bin (not permanent deletion) |
| **📊 View Metadata** | See size, extension, last modified, and last accessed dates |

---

## 🔧 How It Works

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (Browser)                    │
│         HTML5 + CSS3 + Vanilla JavaScript                   │
│            ┌─────────────────────────────┐                  │
│            │   index.html  │  styles.css  │                 │
│            │         script.js           │                  │
│            └─────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼ HTTP/REST
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend (Python)                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ app.py                                               │   │
│  │  - GET  /api/scan         (File scanning)           │   │
│  │  - GET  /api/models       (List Ollama models)      │   │
│  │  - POST /api/summarize    (AI analysis)             │   │
│  │  - GET  /api/open         (Open file)               │   │
│  │  - GET  /api/open-location (Open folder)            │   │
│  │  - DELETE /api/delete     (Trash file)              │   │
│  │  - GET  /api/folders      (Folder sizes)            │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────────┐
│      scanner.py         │     │        analyzer.py           │
│  - Fast scan (7 dirs)   │     │  - Text extraction           │
│  - Advanced scan (35+)  │     │    (pdf, docx, txt, xlsx)    │
│  - Safe-to-delete check │     │  - Ollama LLM integration    │
│  - System file exclusion│     │  - AI summarization          │
└─────────────────────────┘     └─────────────────────────────┘
                                              │
                                              ▼
                                ┌─────────────────────────┐
                                │      Ollama (Local)     │
                                │  Llama 3, Mistral,      │
                                │  Qwen, etc.             │
                                └─────────────────────────┘
```

### Scanning Process

1. **User selects scan mode** (Fast or Advanced)
2. **Scanner traverses directories** and collects files ≥10MB
3. **Metadata collected** including **Last Modified** and **Last Accessed** dates
4. **Safe-to-delete analysis** based on extension and path patterns
5. **Results sorted** to prioritize largest and oldest files
6. **User can analyze** individual files with local AI

### AI Analysis Flow

1. **Text extraction** from supported file formats
2. **Content truncated** to 4000 characters for efficiency  
3. **Prompt sent** to local Ollama model
4. **Summary generated** with importance rating and recommendation
5. **Results displayed** in the file detail panel

---



---

## 🚀 Installation

### Prerequisites

| Requirement | Version | Purpose |
|:------------|:--------|:--------|
| **Python** | 3.8+ | Runtime environment |
| **Ollama** | Latest | Local AI inference |
| **pip** | Latest | Package management |

### Step-by-Step Setup

#### 1. Install Ollama

Download and install from [ollama.com](https://ollama.com), then pull a model:

```bash
# Recommended for fast responses
ollama pull qwen2.5-coder:1.5b

# Or for better analysis quality
ollama pull llama3.2
```

#### 2. Clone the Repository

```bash
git clone https://github.com/ThisisOmar-here/cleaniq.git
cd cleaniq
```

#### 3. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

#### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies:**
| Package | Version | Purpose |
|:--------|:--------|:--------|
| `fastapi` | 0.109.0 | Web framework |
| `uvicorn[standard]` | 0.27.0 | ASGI server |
| `ollama` | 0.1.6 | Ollama Python client |
| `pypdf` | 4.0.1 | PDF text extraction |
| `python-docx` | 1.1.0 | Word document parsing |
| `pandas` | 2.1.4 | Excel/CSV processing |
| `openpyxl` | 3.1.2 | Excel file support |
| `send2trash` | 1.8.3 | Safe file deletion |

#### 5. Run the Application

```bash
uvicorn app:app --reload
```

#### 6. Open in Browser

Navigate to **http://localhost:8000**

---

## 📚 API Reference

### Endpoints

<details>
<summary><strong>GET /api/scan</strong> — Scan for large files</summary>

**Parameters:**
| Name | Type | Required | Description |
|:-----|:-----|:---------|:------------|
| `mode` | string | No | `fast` (default) or `advance` |
| `path` | string | No | Custom path for advanced scan |
| `exclude_system` | boolean | No | Exclude system files (default: false) |

**Response:**
```json
{
  "mode": "fast",
  "path": "Common Folders (7 locations)",
  "file_count": 45,
  "safe_count": 12,
  "total_size": 5368709120,
  "files": [
    {
      "path": "C:\\Users\\...",
      "name": "video.mp4",
      "extension": ".mp4",
      "size_bytes": 1073741824,
      "size_readable": "1.0 GB",
      "modified": "2024-01-15T10:30:00",
      "accessed": "2024-01-20T14:22:00",
      "can_summarize": false,
      "safe_to_delete": false
    }
  ]
}
```
</details>

<details>
<summary><strong>GET /api/models</strong> — List available Ollama models</summary>

**Response:**
```json
{
  "models": [
    {
      "name": "llama3.2",
      "size": 4700000000,
      "modified": "2024-01-10T..."
    }
  ]
}
```
</details>

<details>
<summary><strong>POST /api/summarize</strong> — AI file analysis</summary>

**Request Body:**
```json
{
  "filepath": "C:\\Users\\..\\document.pdf",
  "model": "llama3.2"
}
```

**Response:**
```json
{
  "filepath": "C:\\Users\\..\\document.pdf",
  "success": true,
  "text_preview": "First 500 characters...",
  "summary": "This is a contract document from 2023...",
  "error": null
}
```
</details>

<details>
<summary><strong>GET /api/open</strong> — Open file with default app</summary>

**Parameters:**
| Name | Type | Required | Description |
|:-----|:-----|:---------|:------------|
| `filepath` | string | Yes | Full path to file |

</details>

<details>
<summary><strong>GET /api/open-location</strong> — Open file's folder</summary>

**Parameters:**
| Name | Type | Required | Description |
|:-----|:-----|:---------|:------------|
| `filepath` | string | Yes | Full path to file |

</details>

<details>
<summary><strong>DELETE /api/delete</strong> — Delete file (to Recycle Bin)</summary>

**Parameters:**
| Name | Type | Required | Description |
|:-----|:-----|:---------|:------------|
| `filepath` | string | Yes | Full path to file |

</details>

---

## 💡 Use Cases

| Problem | CleanIQ Solution |
|:--------|:-----------------|
| **"What is `Document_final_v2.pdf`?"** | AI reads it and tells you: *"This is an old contract from 2022."* |
| **"Is this safe to delete?"** | AI advises: *"Safe to delete - appears to be a temporary log file."* |
| **"Where is all my space going?"** | Sort by size to instantly find the biggest storage hogs |
| **"I'm worried about privacy."** | Zero data upload. Works 100% offline with your local LLM |
| **"I have dev tools eating my disk"** | Advanced scan finds npm, nuget, docker, and other dev caches |

---

## 🛠️ Technology Stack

### Backend
- **Python 3.8+** — Core programming language
- **FastAPI** — Modern, fast web framework
- **Uvicorn** — Lightning-fast ASGI server

### Frontend
- **HTML5** — Semantic markup
- **CSS3** — Apple-inspired design system with CSS variables
- **Vanilla JavaScript** — No framework overhead

### AI Engine
- **Ollama** — Local LLM runtime
- **Supported Models** — Llama 3, Mistral, Qwen, and more

### Text Extraction
- **pypdf** — PDF parsing
- **python-docx** — Word documents
- **pandas + openpyxl** — Excel/CSV files

---

## 🤝 Contributing

We welcome contributions! Please read our guidelines before submitting.

### Quick Start

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR-USERNAME/cleaniq.git`
3. **Create a branch**: `git checkout -b feature/amazing-feature`  
4. **Make changes** and commit: `git commit -m "Add amazing feature"`
5. **Push**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Guidelines

- Follow **PEP 8** for Python code
- Use **type hints** for function signatures
- Write **docstrings** for all functions
- Keep commits **focused** and **descriptive**

📖 See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

📜 Read our [Code of Conduct](CODE_OF_CONDUCT.md) for community standards.

---

## 🔒 Security

CleanIQ is designed with security and privacy as core principles:

| Aspect | Implementation |
|:-------|:---------------|
| **Local Processing** | All AI analysis happens on your machine |
| **No Cloud Uploads** | Your files never leave your computer |
| **Safe Deletion** | Files go to Recycle Bin by default |
| **System Protection** | Critical system folders are excluded |

🛡️ Found a vulnerability? Please read our [Security Policy](SECURITY.md).

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 ThisisOmar-here

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🙏 Acknowledgments

- **[Ollama](https://ollama.com)** — Making local LLMs accessible
- **[FastAPI](https://fastapi.tiangolo.com)** — The excellent Python web framework
- **[Inter Font](https://fonts.google.com/specimen/Inter)** — Beautiful typography
- **Apple Design Guidelines** — UI/UX inspiration

---

## 👨‍💻 Author

<p align="center">
  <strong>Made with ❤️ by ThisisOmar-here</strong>
</p>

<p align="center">
  <a href="https://github.com/ThisisOmar-here">
    <img src="https://img.shields.io/badge/GitHub-ThisisOmar--here-181717?style=for-the-badge&logo=github" alt="GitHub">
  </a>
</p>

---

<p align="center">
  ⭐ If CleanIQ helped you, please consider giving it a star!
</p>
