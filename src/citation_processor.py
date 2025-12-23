"""
Citation Processor Module
Handles citation processing and formatting
"""
import requests
import re
from typing import Dict, Any
import config


class CitationProcessor:
    """Processes and formats citations"""
    
    @staticmethod
    def add_citations_to_text(text: str, references: str) -> str:
        """
        Add inline citations to text using OpenRouter API
        
        Args:
            text: Text to add citations to
            references: Reference list
            
        Returns:
            Text with citations added
        """
        if not config.OPENROUTER_API_KEY:
            # Fallback: simple citation addition
            return text
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an academic assistant. Given a paragraph and a list of references in IEEE format, insert relevant inline citations using [1], [2], etc. Do not make up citations. Only use the provided reference list. If unsure, skip citing."
                },
                {
                    "role": "user",
                    "content": f"Paragraph:\n{text}\n\nReferences:{references}"
                }
            ],
            "temperature": 0.2
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            cited_text = result["choices"][0]["message"]["content"]
            
            return cited_text
        except Exception as e:
            print(f"Error adding citations: {e}")
            return text
    
    @staticmethod
    def convert_citations_to_latex(text: str) -> str:
        """
        Convert [1], [2] style citations to LaTeX \\cite format
        
        Args:
            text: Text with [1], [2] citations
            
        Returns:
            Text with LaTeX citations
        """
        # Replace [1], [2] with \cite{r1}, \cite{r2}
        pattern = r'\[(\d+)\]'
        replacement = r'\\cite{r\1}'
        
        return re.sub(pattern, replacement, text)
    
    @staticmethod
    def clean_references(references: str) -> str:
        """
        Clean reference text (remove code blocks, etc.)
        
        Args:
            references: Raw reference text
            
        Returns:
            Cleaned reference text
        """
        cleaned = references.replace("```latex", "").replace("```", "").strip()
        cleaned = cleaned.replace("\\n", "\n")
        return cleaned

