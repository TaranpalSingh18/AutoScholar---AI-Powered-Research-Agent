"""
AI Agents Module
Contains all AI-powered agents for research paper generation
"""
from openai import OpenAI
from typing import Dict, Any, List
import config


class AIAgent:
    """Base class for AI agents"""
    
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.OPENAI_MODEL
    
    def generate(self, prompt: str, system_message: str = "") -> str:
        """
        Generate text using OpenAI API
        
        Args:
            prompt: User prompt
            system_message: System message for context
            
        Returns:
            Generated text
        """
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7
        )
        
        return response.choices[0].message.content


class AbstractWriter(AIAgent):
    """Generates research paper abstracts"""
    
    SYSTEM_MESSAGE = """You are a scientific writing assistant that specializes in generating high-quality research abstracts.
Given:

1. A research topic,

2. A brief description of the proposed work, and

3. Summaries of five relevant research papers,

your task is to write a concise and coherent abstract suitable for an academic paper.
The abstract should clearly state the motivation, problem, methods, and expected contributions of the proposed work.
Use formal academic language. Do not copy content directly from the referenced summaries—synthesize and relate ideas meaningfully."""
    
    def write_abstract(self, topic: str, description: str, paper_summaries: List[Dict[str, str]]) -> str:
        """
        Generate abstract
        
        Args:
            topic: Research topic
            description: Research description
            paper_summaries: List of paper summaries with title and summary
            
        Returns:
            Generated abstract
        """
        prompt = f"Topic of Research: {topic}\n"
        prompt += f"Description of Research: {description}\n"
        prompt += "Summary of Papers:\n"
        
        for i, paper in enumerate(paper_summaries[:5], 1):
            prompt += f"{i}.\n"
            prompt += f"Title : {paper.get('title', '')}\n"
            prompt += f"Summary : {paper.get('summary', '')}\n"
        
        return self.generate(prompt, self.SYSTEM_MESSAGE)


class IntroductionWriter(AIAgent):
    """Generates research paper introductions"""
    
    SYSTEM_MESSAGE = """You are an academic writing assistant that drafts the introduction section of a research paper.
Given:

The research topic,

A brief description of the proposed work, and

Summaries of five relevant research papers (including titles and authors),

write a formal and structured introduction.
Focus on:
– Outlining the broader research area,
– Highlighting general trends, recent advancements, and common challenges from the referenced works,
– Avoiding deep technical details or analysis of individual papers (a separate literature survey will handle that),
– Clearly stating the research gap and the motivation for the proposed work.
Use formal academic tone with clear, concise language and logical flow.
-Cite paper with provided authors where needed"""
    
    def write_introduction(self, topic: str, description: str, paper_summaries: List[Dict[str, str]]) -> str:
        """
        Generate introduction
        
        Args:
            topic: Research topic
            description: Research description
            paper_summaries: List of paper summaries with title, summary, and authors
            
        Returns:
            Generated introduction
        """
        prompt = f"Topic of Research: {topic}\n"
        prompt += f"Description of Research: {description}\n"
        prompt += "Summary of Papers:\n"
        
        for i, paper in enumerate(paper_summaries[:5], 1):
            prompt += f"{i}.\n"
            prompt += f"Title : {paper.get('title', '')}\n"
            prompt += f"Summary : {paper.get('summary', '')}\n"
            prompt += f"Authors : {paper.get('authors', '')}\n\n"
        
        return self.generate(prompt, self.SYSTEM_MESSAGE)


class LiteratureReviewer(AIAgent):
    """Generates literature review sections"""
    
    SYSTEM_MESSAGE = """You are a research assistant that writes the literature survey section of a research paper.
You will receive:
– A research topic and description,
– Summaries of five relevant research papers, each including title, authors, technique used, database used, accuracy/measures, and remarks.

Your task is to:

Write a brief literature survey paragraph (~100 words) that summarizes general trends, methodologies, and gaps based on the reviewed works. Do not go deep into individual papers — just synthesize common findings.

Follow this with a LaTeX-formatted table that summarizes the five papers using these column headers:

Reviewed Paper

Technique Used

Database Used

Accuracy Measures

Remarks

Format the table using the tabular environment inside a table block. Use the following column specification to ensure it fits in a single-column layout:
|p{1.3cm}|p{1.3cm}|p{1.3cm}|p{1.3cm}|p{1.3cm}|

Use \\textbf{} for headers and align content properly.
Output only the LaTeX code, ready to paste directly into a LaTeX document.
Ensure both the paragraph and table appear as valid LaTeX."""
    
    def write_literature_review(self, topic: str, description: str, paper_summaries: List[Dict[str, str]]) -> str:
        """
        Generate literature review
        
        Args:
            topic: Research topic
            description: Research description
            paper_summaries: List of paper summaries
            
        Returns:
            Generated literature review in LaTeX format
        """
        prompt = f"Topic of Research: {topic}\n"
        prompt += f"Description of Research: {description}\n"
        prompt += "Summary of Papers:\n"
        
        for i, paper in enumerate(paper_summaries[:5], 1):
            prompt += f"{i}.\n"
            prompt += f"Title : {paper.get('title', '')}\n"
            prompt += f"Summary : {paper.get('summary', '')}\n"
            prompt += f"Authors : {paper.get('authors', '')}\n\n"
        
        return self.generate(prompt, self.SYSTEM_MESSAGE)


class ReferenceAgent(AIAgent):
    """Generates IEEE-style references in LaTeX format"""
    
    SYSTEM_MESSAGE = """You are a reference formatting assistant that outputs citations in LaTeX code using IEEE style.
Given the title, authors, publication year, and (if available) the journal/conference name, volume/issue/pages, and URL/DOI, generate references in the following format:

\\bibitem{r1}
Author(s). (Year). Title of the paper. \\textit{Journal/Conference Name}, \\textbf{Volume}(Issue), Page range. 
\\url{DOI or URL}

Guidelines:
– Format author names as "Lastname, First Initial." and separate multiple authors with commas; use "et al." if more than 4 authors.
– Capitalize major words in the title and put it in sentence case.
– Use \\textit{} for journal/conference names and \\textbf{} for volume number.
– Use \\url{} to enclose the DOI or URL.
– Number each entry as \\bibitem{r1}, \\bibitem{r2}, etc.

Output only the LaTeX code starting with \\bibitem{r1}, ready to paste into the \\begin{thebibliography} section of a research paper."""
    
    def generate_references(self, papers: List[Dict[str, str]]) -> str:
        """
        Generate IEEE-style references
        
        Args:
            papers: List of paper dictionaries with title, authors, link, and publish date
            
        Returns:
            LaTeX-formatted references
        """
        prompt = "Reference Papers :\n"
        
        for i, paper in enumerate(papers[:5], 1):
            publish_year = paper.get('published', '')[:4] if paper.get('published') else ''
            prompt += f"{i}.\n"
            prompt += f"Title : {paper.get('title', '')}\n"
            prompt += f"Author : {paper.get('authors', '')}\n"
            prompt += f"Link : {paper.get('id', '')}\n"
            prompt += f"Publish year : {publish_year}\n"
        
        output = self.generate(prompt, self.SYSTEM_MESSAGE)
        
        # Clean up output and wrap in bibliography environment
        cleaned = output.replace("```latex", "").replace("```", "").strip()
        cleaned = cleaned.replace("\\n", "\n")
        
        bibliography = f"\\begin{{thebibliography}}{{99}}\n\n{cleaned}\n\n\\end{{thebibliography}}"
        
        return bibliography


class CitationAgent(AIAgent):
    """Generates IEEE citation format"""
    
    SYSTEM_MESSAGE = """You are a reference formatting assistant specialized in generating bibliographic entries in IEEE citation style.
You will receive the title, author(s), paper url and publication year of each paper.
Your task is to:
– Format each entry according to the IEEE style guide,
– Ensure correct author formatting (e.g., "A. B. Lastname"),
– Enclose the title in quotation marks and capitalize major words,
– Format journal/conference names (if given) in italics (you may omit them if not provided),
– Number entries [1], [2], etc., for direct placement in the reference section.

Output strictly in form of array only [   "[1] S. Nayak, R. Patgiri, L. Waikhom, and A. Ahmed, "A Review on Edge Analytics: Issues, Challenges, Opportunities, Promises, Future Directions, and Applications," 2023.",   "[2] S. Mhamudul Hasan, A. M. Alotaibi, S. Talukder, and A. R. Shahid, "Distributed Threat Intelligence at the Edge Devices: A Large Language Model-Driven Approach," 2023.",   "[3] K. Zhang, G. Li, N. Lu, P. Yang, and K. Tang, "Hardware-Aware DNN Compression for Homogeneous Edge Devices," 2023.",   "[4] X. Guo, A. D. Pimentel, and T. Stefanov, "AutoDiCE: Fully Automated Distributed CNN Inference at the Edge," 2023.",   "[5] P. Subedi, J. Hao, I. K. Kim, and L. Ramaswamy, "AI Multi-Tenancy on Edge: Concurrent Deep Learning Model Executions and Dynamic Model Placements on Edge Devices," 2023." ]

"""
    
    def generate_citations(self, papers: List[Dict[str, str]]) -> List[str]:
        """
        Generate IEEE citations
        
        Args:
            papers: List of paper dictionaries
            
        Returns:
            List of citation strings
        """
        prompt = "Reference Papers :\n"
        
        for i, paper in enumerate(papers[:5], 1):
            publish_year = paper.get('published', '')[:4] if paper.get('published') else ''
            prompt += f"{i}.\n"
            prompt += f"Title : {paper.get('title', '')}\n"
            prompt += f"Author : {paper.get('authors', '')}\n"
            prompt += f"Link : {paper.get('id', '')}\n"
            prompt += f"Publish year : {publish_year}\n"
        
        output = self.generate(prompt, self.SYSTEM_MESSAGE)
        
        # Parse array output
        import json
        import re
        
        # Try to extract JSON array
        try:
            # Find array in output
            array_match = re.search(r'\[.*\]', output, re.DOTALL)
            if array_match:
                citations = json.loads(array_match.group())
                return citations
        except:
            pass
        
        # Fallback: split by lines and clean
        citations = []
        for line in output.split('\n'):
            line = line.strip()
            if line.startswith('[') and ']' in line:
                citations.append(line)
        
        return citations if citations else [output]


class MethodologyAgent(AIAgent):
    """Generates methodology sections"""
    
    SYSTEM_MESSAGE = """You are a research writing assistant that generates the methodology section of a research paper.
You will receive:
– The abstract of the proposed research,
– A literature review summarizing existing techniques and gaps, and
– Human input providing guidance or constraints (e.g., specific tools, models, datasets, or approaches to be used).

Your task is to:
– Formulate a detailed and technically sound methodology to fulfill the research goals stated in the abstract,
– use references from the literature review,
– Incorporate the human-provided instructions as priority constraints,
– Use accurate technical terminology and structure the response in logical steps or modules (e.g., data collection, preprocessing, model design, evaluation),
– Clearly justify why each step is included.

Maintain a formal academic tone suitable for publication.
Dont start with a heading Methodology"""
    
    def write_methodology(self, topic: str, abstract: str, literature_review: str, human_input: str = "") -> str:
        """
        Generate methodology
        
        Args:
            topic: Research topic
            abstract: Research abstract
            literature_review: Literature review section
            human_input: Human-provided methodology guidance
            
        Returns:
            Generated methodology section
        """
        prompt = f"Topic of Research : {topic}\n"
        prompt += f"Abstract : {abstract}\n"
        prompt += f"Literature Review : {literature_review}\n"
        prompt += f"Human Input : {human_input}"
        
        return self.generate(prompt, self.SYSTEM_MESSAGE)


class FlowchartAgent(AIAgent):
    """Generates Graphviz DOT diagrams from methodology"""
    
    SYSTEM_MESSAGE = """You are a technical writer. Convert the given methodology into a Graphviz DOT diagram showing steps and flow

Return the DOT code only without triple quotes at start and end, enclosed in triple backticks."""
    
    def generate_flowchart(self, methodology: str) -> str:
        """
        Generate Graphviz DOT code from methodology
        
        Args:
            methodology: Methodology text
            
        Returns:
            Graphviz DOT code
        """
        prompt = f"Methodology : {methodology}"
        
        output = self.generate(prompt, self.SYSTEM_MESSAGE)
        
        # Clean up output
        cleaned = output.replace("```dot", "").replace("```", "").strip()
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
            else:
                formatted_lines.append(line + ";")
        
        return "\n".join(formatted_lines)

