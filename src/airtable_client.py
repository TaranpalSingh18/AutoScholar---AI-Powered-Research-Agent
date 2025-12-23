"""
Airtable Integration Module
Handles all Airtable operations for storing research data
"""
from pyairtable import Api
from typing import Dict, Any, List
import config


class AirtableClient:
    """Client for Airtable operations"""
    
    def __init__(self):
        self.api = Api(config.AIRTABLE_API_KEY)
        self.base_id = config.AIRTABLE_BASE_ID
        self.reference_table = self.api.table(
            self.base_id,
            config.AIRTABLE_REFERENCE_TABLE_ID
        )
        self.research_table = self.api.table(
            self.base_id,
            config.AIRTABLE_RESEARCH_TABLE_ID
        )
    
    def create_reference_paper(self, paper_data: Dict[str, Any], topic: str, description: str) -> Dict[str, Any]:
        """
        Create a reference paper record
        
        Args:
            paper_data: Paper data dictionary
            topic: Research topic
            description: Research description
            
        Returns:
            Created record
        """
        record = {
            "TItle": paper_data.get("title", ""),
            "Summary": paper_data.get("summary", ""),
            "Authors": paper_data.get("authorsFormatted", ""),
            "Link": paper_data.get("id", ""),
            "Topic": topic,
            "Description": description,
            "Publish Date": paper_data.get("published", "")
        }
        
        return self.reference_table.create(record)
    
    def create_research_paper(self, topic_name: str) -> Dict[str, Any]:
        """
        Create a research paper record
        
        Args:
            topic_name: Topic name
            
        Returns:
            Created record
        """
        record = {
            "Topic Name": topic_name
        }
        
        return self.research_table.create(record)
    
    def update_research_paper(self, topic_name: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a research paper record
        
        Args:
            topic_name: Topic name to match
            updates: Dictionary of fields to update
            
        Returns:
            Updated record
        """
        # Find record by topic name
        records = self.research_table.all(formula=f"{{Topic Name}} = '{topic_name}'")
        
        if not records:
            raise ValueError(f"No record found with topic name: {topic_name}")
        
        record_id = records[0]["id"]
        
        # Prepare update fields
        update_fields = {}
        if "Abstract" in updates:
            update_fields["Abstract"] = updates["Abstract"]
        if "Introduction" in updates:
            update_fields["Introduction"] = updates["Introduction"]
        if "Literature Review" in updates:
            update_fields["Literature Review"] = updates["Literature Review"]
        if "Methodology" in updates:
            update_fields["Methodology"] = updates["Methodology"]
        if "Results" in updates:
            update_fields["Results"] = updates["Results"]
        if "Conclusion" in updates:
            update_fields["Conclusion"] = updates["Conclusion"]
        
        return self.research_table.update(record_id, update_fields)
    
    def get_reference_papers_by_topic(self, topic: str) -> List[Dict[str, Any]]:
        """
        Get all reference papers for a topic
        
        Args:
            topic: Research topic
            
        Returns:
            List of reference paper records
        """
        records = self.reference_table.all(formula=f"{{Topic}} = '{topic}'")
        return records

