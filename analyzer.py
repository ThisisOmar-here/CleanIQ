"""
File Analyzer Module
Extracts text content from files and generates summaries using Ollama.
"""

import os
from pathlib import Path
from typing import Optional, List, Dict, Any

# Text extraction imports
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

try:
    from docx import Document
except ImportError:
    Document = None

try:
    import pandas as pd
except ImportError:
    pd = None

# Ollama integration
try:
    import ollama
except ImportError:
    ollama = None


def get_available_models() -> List[Dict[str, Any]]:
    """Get list of available Ollama models."""
    if ollama is None:
        return []
    
    try:
        response = ollama.list()
        models = []
        for model in response.get('models', []):
            models.append({
                "name": model.get('name', ''),
                "size": model.get('size', 0),
                "modified": model.get('modified_at', ''),
            })
        return models
    except Exception as e:
        print(f"Error fetching Ollama models: {e}")
        return []


def extract_text_from_pdf(filepath: str, max_pages: int = 10) -> Optional[str]:
    """Extract text content from a PDF file."""
    if PdfReader is None:
        return None
    
    try:
        reader = PdfReader(filepath)
        text_parts = []
        for i, page in enumerate(reader.pages[:max_pages]):
            text_parts.append(page.extract_text() or '')
        return '\n'.join(text_parts)
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None


def extract_text_from_docx(filepath: str) -> Optional[str]:
    """Extract text content from a DOCX file."""
    if Document is None:
        return None
    
    try:
        doc = Document(filepath)
        paragraphs = [p.text for p in doc.paragraphs]
        return '\n'.join(paragraphs)
    except Exception as e:
        print(f"Error reading DOCX: {e}")
        return None


def extract_text_from_txt(filepath: str) -> Optional[str]:
    """Extract text content from a TXT file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading TXT: {e}")
        return None


def extract_text_from_excel(filepath: str) -> Optional[str]:
    """Extract text content from Excel files."""
    if pd is None:
        return None
    
    try:
        df = pd.read_excel(filepath, sheet_name=0, nrows=100)
        return df.to_string()
    except Exception as e:
        print(f"Error reading Excel: {e}")
        return None


def extract_text(filepath: str) -> Optional[str]:
    """
    Extract text from a file based on its extension.
    
    Args:
        filepath: Path to the file
        
    Returns:
        Extracted text content or None if extraction fails
    """
    ext = Path(filepath).suffix.lower()
    
    extractors = {
        '.pdf': extract_text_from_pdf,
        '.docx': extract_text_from_docx,
        '.doc': extract_text_from_docx,
        '.txt': extract_text_from_txt,
        '.xlsx': extract_text_from_excel,
        '.xls': extract_text_from_excel,
        '.csv': lambda f: extract_text_from_txt(f),  # CSV as text
    }
    
    extractor = extractors.get(ext)
    if extractor:
        return extractor(filepath)
    return None


def summarize_content(text: str, model: str = "llama3.2") -> Optional[str]:
    """
    Generate a summary of text content using Ollama.
    
    Args:
        text: Text content to summarize
        model: Ollama model name to use
        
    Returns:
        Summary text or None if summarization fails
    """
    if ollama is None:
        return "Ollama not available. Please install and run Ollama."
    
    if not text or len(text.strip()) < 50:
        return "File content is too short to summarize."
    
    # Truncate very long texts to improve speed
    max_chars = 4000
    if len(text) > max_chars:
        text = text[:max_chars] + "...[truncated]"
    
    prompt = f"""Summarize this document in 1 simple sentence.
Do not output any reasoning or thoughts.
Directly answer with the summary, importance level, and recommendation.

Content:
{text}"""

    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            options={"num_predict": 512}  # Increase limit to allow "thinking" to finish
        )
        content = response['message']['content']
        
        # Clean up <think> blocks
        # Handle case where </think> works
        if "</think>" in content:
            content = content.split("</think>")[-1]
            
        # Regex fallback for other variations
        import re
        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
        content = re.sub(r'<think>.*', '', content, flags=re.DOTALL) # Remove unclosed think blocks at end
            
        return content.strip()
    except Exception as e:
        return f"Error: {str(e)}"


def analyze_file(filepath: str, model: str = "llama3.2") -> Dict[str, Any]:
    """
    Full analysis of a file: extract text and generate summary.
    
    Args:
        filepath: Path to the file
        model: Ollama model to use
        
    Returns:
        Dictionary with analysis results
    """
    result = {
        "filepath": filepath,
        "success": False,
        "text_preview": None,
        "summary": None,
        "error": None,
    }
    
    # Extract text
    text = extract_text(filepath)
    if text is None:
        result["error"] = "Could not extract text from this file type."
        return result
    
    # Store preview
    result["text_preview"] = text[:500] + "..." if len(text) > 500 else text
    
    # Generate summary
    summary = summarize_content(text, model)
    result["summary"] = summary
    result["success"] = True
    
    return result
