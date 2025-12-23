"""
Main Workflow Orchestrator
Coordinates all components to execute the research paper generation workflow
"""
from typing import Dict, Any, List, Optional
from src.arxiv_fetcher import ArxivFetcher
from src.ai_agents import (
    AbstractWriter,
    IntroductionWriter,
    LiteratureReviewer,
    ReferenceAgent,
    CitationAgent,
    MethodologyAgent,
    FlowchartAgent
)
from src.airtable_client import AirtableClient
from src.github_client import GitHubClient
from src.latex_generator import LaTeXGenerator
from src.citation_processor import CitationProcessor
from src.flowchart_generator import FlowchartGenerator
from src.email_client import EmailClient


class ResearchWorkflow:
    """Main workflow orchestrator"""
    
    def __init__(self):
        self.arxiv_fetcher = ArxivFetcher()
        self.abstract_writer = AbstractWriter()
        self.introduction_writer = IntroductionWriter()
        self.literature_reviewer = LiteratureReviewer()
        self.reference_agent = ReferenceAgent()
        self.citation_agent = CitationAgent()
        self.methodology_agent = MethodologyAgent()
        self.flowchart_agent = FlowchartAgent()
        self.airtable = AirtableClient()
        self.github = GitHubClient()
        self.citation_processor = CitationProcessor()
        self.flowchart_generator = FlowchartGenerator()
        self.email_client = EmailClient()
    
    def execute(self, topic: str, description: str, methodology_input: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute the complete research workflow
        
        Args:
            topic: Research topic
            description: Research description
            methodology_input: Optional human-provided methodology input
            
        Returns:
            Dictionary containing all generated content and file paths
        """
        result = {
            "topic": topic,
            "description": description,
            "papers": [],
            "abstract": "",
            "introduction": "",
            "literature_review": "",
            "methodology": "",
            "references": "",
            "citations": [],
            "latex": "",
            "flowchart_url": "",
            "success": False
        }
        
        try:
            # Step 1: Fetch papers from arXiv
            print("Fetching papers from arXiv...")
            feed_data = self.arxiv_fetcher.fetch_papers(topic, max_results=5)
            entries = self.arxiv_fetcher.extract_entries(feed_data)
            
            # Process entries
            papers = []
            for entry in entries:
                processed = self.arxiv_fetcher.process_entry(entry)
                papers.append(processed)
                
                # Store in Airtable
                try:
                    self.airtable.create_reference_paper(processed, topic, description)
                except Exception as e:
                    print(f"Warning: Could not save to Airtable: {e}")
            
            result["papers"] = papers
            
            # Step 2: Create research paper record in Airtable
            print("Creating research paper record...")
            try:
                self.airtable.create_research_paper(topic)
            except Exception as e:
                print(f"Warning: Could not create Airtable record: {e}")
            
            # Step 3: Generate Abstract
            print("Generating abstract...")
            paper_summaries = [{"title": p["title"], "summary": p["summary"]} for p in papers]
            abstract = self.abstract_writer.write_abstract(topic, description, paper_summaries)
            result["abstract"] = abstract
            
            # Step 4: Generate Introduction
            print("Generating introduction...")
            intro_papers = [{"title": p["title"], "summary": p["summary"], "authors": p["authors"]} for p in papers]
            introduction = self.introduction_writer.write_introduction(topic, description, intro_papers)
            result["introduction"] = introduction
            
            # Step 5: Generate Literature Review
            print("Generating literature review...")
            literature_review = self.literature_reviewer.write_literature_review(topic, description, intro_papers)
            result["literature_review"] = literature_review
            
            # Step 6: Generate References
            print("Generating references...")
            references = self.reference_agent.generate_references(papers)
            result["references"] = references
            
            # Step 7: Generate Citations
            print("Generating citations...")
            citations = self.citation_agent.generate_citations(papers)
            result["citations"] = citations
            
            # Step 8: Add citations to introduction
            print("Adding citations to introduction...")
            cited_intro = self.citation_processor.add_citations_to_text(introduction, "\n".join(citations))
            cited_intro_latex = self.citation_processor.convert_citations_to_latex(cited_intro)
            
            # Step 9: Request human input for methodology (if email enabled)
            print("Requesting methodology input...")
            human_input = methodology_input
            
            # If no methodology input provided and email is enabled, send request
            if not human_input and self.email_client.enabled:
                # In production, this would wait for webhook response
                # For now, we'll proceed with AI-generated methodology
                print("Email client enabled but no input provided. Using AI-generated methodology.")
            
            # Generate Methodology
            print("Generating methodology...")
            methodology = self.methodology_agent.write_methodology(
                topic, abstract, literature_review, human_input or ""
            )
            result["methodology"] = methodology
            
            # Format methodology for LaTeX
            formatted_methodology = LaTeXGenerator.format_methodology_for_latex(methodology)
            
            # Step 10: Generate Flowchart
            print("Generating flowchart...")
            dot_code = self.flowchart_agent.generate_flowchart(methodology)
            flowchart_url = self.flowchart_generator.generate_flowchart_image(dot_code)
            result["flowchart_url"] = flowchart_url or ""
            
            # Step 11: Generate LaTeX document
            print("Generating LaTeX document...")
            latex = LaTeXGenerator.generate_ieee_paper(
                topic=topic,
                abstract=abstract,
                introduction=cited_intro_latex,
                literature_review=literature_review,
                methodology=formatted_methodology,
                references=references
            )
            result["latex"] = latex
            
            # Step 12: Update Airtable with all content
            print("Updating Airtable...")
            try:
                self.airtable.update_research_paper(topic, {
                    "Abstract": abstract,
                    "Introduction": cited_intro_latex,
                    "Literature Review": literature_review,
                    "Methodology": formatted_methodology
                })
            except Exception as e:
                print(f"Warning: Could not update Airtable: {e}")
            
            # Step 13: Upload to GitHub
            print("Uploading to GitHub...")
            try:
                self.github.upload_latex_paper(topic, latex)
                result["github_url"] = f"https://github.com/{self.github.owner}/{self.github.repo_name}/blob/main/docs/{topic.replace(' ', '_')}.tex"
            except Exception as e:
                print(f"Warning: Could not upload to GitHub: {e}")
            
            result["success"] = True
            print("Workflow completed successfully!")
            
        except Exception as e:
            print(f"Error in workflow execution: {e}")
            import traceback
            traceback.print_exc()
            result["error"] = str(e)
        
        return result

