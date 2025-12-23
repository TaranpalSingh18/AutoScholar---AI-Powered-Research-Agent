"""
GitHub Integration Module
Handles file uploads to GitHub repository
"""
from github import Github
from typing import Optional
import config
import base64


class GitHubClient:
    """Client for GitHub operations"""
    
    def __init__(self):
        self.github = Github(config.GITHUB_TOKEN)
        self.owner = config.GITHUB_OWNER
        self.repo_name = config.GITHUB_REPO
        self.repo = self.github.get_user(self.owner).get_repo(self.repo_name)
    
    def upload_file(self, file_path: str, content: str, commit_message: str = "paper created") -> bool:
        """
        Upload a file to GitHub repository
        
        Args:
            file_path: Path to file in repository (e.g., "docs/paper.tex")
            content: File content as string
            commit_message: Commit message
            
        Returns:
            True if successful
        """
        try:
            # Check if file exists
            try:
                file = self.repo.get_contents(file_path)
                # Update existing file
                self.repo.update_file(
                    file_path,
                    commit_message,
                    content,
                    file.sha
                )
            except:
                # Create new file
                self.repo.create_file(
                    file_path,
                    commit_message,
                    content
                )
            
            return True
        except Exception as e:
            print(f"Error uploading file to GitHub: {e}")
            return False
    
    def upload_latex_paper(self, topic_name: str, latex_content: str) -> bool:
        """
        Upload LaTeX paper to GitHub
        
        Args:
            topic_name: Topic name (used as filename)
            latex_content: LaTeX content
            
        Returns:
            True if successful
        """
        # Sanitize topic name for filename
        safe_filename = "".join(c for c in topic_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_filename = safe_filename.replace(' ', '_')
        file_path = f"docs/{safe_filename}.tex"
        
        return self.upload_file(file_path, latex_content, f"Research paper: {topic_name}")

