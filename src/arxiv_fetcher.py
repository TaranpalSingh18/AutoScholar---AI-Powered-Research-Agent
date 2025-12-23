"""
ArXiv Paper Fetcher Module
Fetches relevant papers from arXiv based on research topic
"""
import requests
import xmltodict
from typing import List, Dict, Any


class ArxivFetcher:
    """Fetches papers from arXiv API"""
    
    BASE_URL = "https://export.arxiv.org/api/query"
    
    @staticmethod
    def fetch_papers(topic: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Fetch papers from arXiv
        
        Args:
            topic: Research topic to search for
            max_results: Maximum number of results to return
            
        Returns:
            Dictionary containing feed data
        """
        params = {
            "search_query": f"all:{topic}",
            "start": 0,
            "max_results": max_results
        }
        
        response = requests.get(ArxivFetcher.BASE_URL, params=params)
        response.raise_for_status()
        
        # Parse XML response
        data = xmltodict.parse(response.text)
        return data
    
    @staticmethod
    def extract_entries(feed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract entries from feed data
        
        Args:
            feed_data: Parsed XML feed data
            
        Returns:
            List of entry dictionaries
        """
        entries = feed_data.get("feed", {}).get("entry", [])
        
        # Ensure entries is a list
        if not isinstance(entries, list):
            entries = [entries]
        
        return entries
    
    @staticmethod
    def format_authors(entry: Dict[str, Any]) -> str:
        """
        Format authors from entry
        
        Args:
            entry: Entry dictionary
            
        Returns:
            Comma-separated string of author names
        """
        authors = entry.get("author", [])
        
        if not isinstance(authors, list):
            authors = [authors]
        
        author_names = []
        for author in authors:
            name = author.get("name", "").strip() if isinstance(author, dict) else str(author).strip()
            if name:
                author_names.append(name)
        
        return ", ".join(author_names)
    
    @staticmethod
    def process_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single entry and format it
        
        Args:
            entry: Raw entry dictionary
            
        Returns:
            Processed entry with formatted fields
        """
        # Extract fields
        title = entry.get("title", "").strip().replace("\n", " ")
        summary = entry.get("summary", "").strip().replace("\n", " ")
        paper_id = entry.get("id", "")
        published = entry.get("published", "")
        authors_formatted = ArxivFetcher.format_authors(entry)
        
        return {
            "title": title,
            "summary": summary,
            "id": paper_id,
            "published": published,
            "authors": authors_formatted,
            "authorsFormatted": authors_formatted
        }

