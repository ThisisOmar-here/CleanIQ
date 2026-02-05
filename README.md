# 🧠 CleanIQ

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg)](https://fastapi.tiangolo.com/)
[![Open Source](https://img.shields.io/badge/Open%20Source-%E2%9D%A4-red.svg)](https://github.com/ThisisOmar-here/cleaniq)

**Your intelligent, privacy-first storage assistant.**

CleanIQ is a modern desktop application that helps you regain control over your digital clutter. Unlike traditional disk cleaners that only look at file sizes, CleanIQ uses **local Artificial Intelligence** to read, analyze, and summarize your files, helping you decide what to keep and what to delete—without your data ever leaving your computer.

---

## ✨ Key Features

### 🔍 Smart Scanning Modes
*   **⚡ Fast Scan**: Instantly checks common clutter locations (Downloads, Desktop, Temp, Documents) to give you quick wins.
*   **🛡️ Advanced Scan**: Deeply scans any folder you choose, recursively finding large files hidden deep in your drive.
*   **System Protection**: Automatically excludes critical system files to prevent accidental damage.

### 🤖 AI-Powered Analysis
Don't just see a filename—understand what's inside.
*   **Instant Summaries**: Click "Analyze with AI" to get a 1-sentence summary of any document (PDF, Word, Text, Excel).
*   **Importance Assessment**: The AI rates files as "High," "Medium," or "Low" importance.
*   **Smart Recommendations**: Get actionable advice like "Keep," "Review," or "Safe to delete."
*   **100% Local & Private**: Powered by **Ollama**, all analysis happens on your machine. No data is ever uploaded to the cloud.

### 🎨 Beautiful, Modern UI
*   **Apple-Inspired Design**: Clean, minimal, and intuitive interface with a glassmorphism sidebar.
*   **Interactive Dashboard**: Sort files by size, date, or name with a single click.
*   **Live Feedback**: Smooth animations and real-time scanning updates.

### ⚡ Powerful File Management
*   **Open Location**: Jumping straight to the file's folder in Explorer with one click.
*   **Instant Preview**: View file metadata (size, last modified, accessed dates) at a glance.
*   **Safe Deletion**: Send unwanted files directly to the Recycle Bin.

---

## 📸 Screenshots

*Coming soon! Screenshots of the application interface will be added here.*

---

## 🚀 How It Helps You

| Problem | The AI Storage Saver Solution |
| :--- | :--- |
| **"What is `Doc1.pdf`?"** | The AI reads it and tells you: *"This is an old receipt from 2022."* |
| **"Is this clear to delete?"** | The AI advises: *"Safe to delete - appears to be a temporary log file."* |
| **"Where is all my space going?"** | Sort by "Size (Largest)" to instantly find the biggest hogs. |
| **"I'm worried about privacy."** | Zero data upload. It works completely offline with your local LLM. |

---

## 🛠️ Technology Stack

*   **Backend**: Python, FastAPI
*   **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
*   **AI Engine**: Ollama (Llama 3, Mistral, Qwen, etc.)
*   **Text Extraction**: `pypdf`, `python-docx`, `pandas`

## 📦 Installation & Setup

1.  **Install Ollama**: Download from [ollama.com](https://ollama.com) and pull a model (e.g., `ollama pull qwen2.5-coder:1.5b`).
2.  **Install Python**: Ensure Python 3.8+ is installed.
3.  **Clone the repository**:
    ```bash
    git clone https://github.com/ThisisOmar-here/cleaniq.git
    cd cleaniq
    ```
4.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
5.  **Run the App**:
    ```bash
    uvicorn app:app --reload
    ```
6.  **Open Browser**: Navigate to `http://localhost:8000`

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting a Pull Request.

See the [Code of Conduct](CODE_OF_CONDUCT.md) for community guidelines.

---

## 🔒 Security

For security concerns, please review our [Security Policy](SECURITY.md).

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Created By

Made with ❤️ by Omar Barghouthi
*   [GitHub Profile](https://github.com/ThisisOmar-here)
