"""
Flowchart Generator Module
Generates flowcharts from methodology using Graphviz
"""
import requests
from typing import Optional
from urllib.parse import quote


class FlowchartGenerator:
    """Generates flowcharts from Graphviz DOT code"""
    
    @staticmethod
    def generate_flowchart_image(dot_code: str) -> Optional[str]:
        """
        Generate flowchart image URL from DOT code
        
        Args:
            dot_code: Graphviz DOT code
            
        Returns:
            URL to generated image or None if error
        """
        try:
            # Clean DOT code
            cleaned = dot_code.replace("```dot", "").replace("```", "").strip()
            cleaned = cleaned.replace("\\n", "\n")
            
            # Ensure proper formatting
            lines = cleaned.split("\n")
            formatted_lines = []
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if line.endswith(";") or line.endswith("{") or line.endswith("}"):
                    formatted_lines.append(line)
                elif not line.startswith("digraph") and not line.startswith("graph"):
                    formatted_lines.append(line + ";")
                else:
                    formatted_lines.append(line)
            
            dot_final = "\n".join(formatted_lines)
            
            # Encode and create URL
            encoded = quote(dot_final)
            image_url = f"https://quickchart.io/graphviz?graph={encoded}"
            
            return image_url
        except Exception as e:
            print(f"Error generating flowchart: {e}")
            return None
    
    @staticmethod
    def download_flowchart_image(image_url: str) -> Optional[bytes]:
        """
        Download flowchart image
        
        Args:
            image_url: URL to flowchart image
            
        Returns:
            Image bytes or None if error
        """
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            return response.content
        except Exception as e:
            print(f"Error downloading flowchart: {e}")
            return None

