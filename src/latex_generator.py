"""
LaTeX Generator Module
Generates LaTeX documents in IEEE format
"""
from typing import Dict, Any
import config


class LaTeXGenerator:
    """Generates LaTeX documents"""
    
    @staticmethod
    def escape_latex(text: str) -> str:
        """
        Escape special LaTeX characters
        
        Args:
            text: Text to escape
            
        Returns:
            Escaped text
        """
        # Escape special characters first (before handling newlines)
        special_chars = {
            "\\": "\\textbackslash{}",  # Must be first to avoid double-escaping
            "&": "\\&",
            "%": "\\%",
            "$": "\\$",
            "#": "\\#",
            "^": "\\textasciicircum{}",
            "_": "\\_",
            "{": "\\{",
            "}": "\\}",
            "~": "\\textasciitilde{}"
        }
        
        for char, replacement in special_chars.items():
            text = text.replace(char, replacement)
        
        # Replace newlines with double backslashes for LaTeX line breaks
        text = text.replace("\n", "\\\\")
        
        return text
    
    @staticmethod
    def generate_ieee_paper(
        topic: str,
        abstract: str,
        introduction: str,
        literature_review: str,
        methodology: str,
        references: str,
        authors: list = None
    ) -> str:
        """
        Generate IEEE format LaTeX document
        
        Args:
            topic: Paper topic/title
            abstract: Abstract text
            introduction: Introduction text
            literature_review: Literature review text
            methodology: Methodology text
            references: References in LaTeX format
            authors: List of author dictionaries (uses config if None)
            
        Returns:
            Complete LaTeX document
        """
        if authors is None:
            authors = config.AUTHORS
        
        # Escape LaTeX special characters
        topic_escaped = LaTeXGenerator.escape_latex(topic)
        abstract_escaped = LaTeXGenerator.escape_latex(abstract)
        introduction_escaped = LaTeXGenerator.escape_latex(introduction)
        literature_review_escaped = LaTeXGenerator.escape_latex(literature_review)
        methodology_escaped = LaTeXGenerator.escape_latex(methodology)
        
        # Generate author block
        author_blocks = []
        for i, author in enumerate(authors):
            author_block = f"\\IEEEauthorblockN{{{author['name']}}}\n"
            author_block += f"\\IEEEauthorblockA{{{author['department']}\n"
            author_block += f"\\\\{author['institution']}\n"
            author_block += f"\\\\{author['location']}\n"
            author_block += f"\\\\Email: {author['email']}}}"
            
            if i < len(authors) - 1:
                author_block += "\n\\and\n"
            
            author_blocks.append(author_block)
        
        authors_text = "\n".join(author_blocks)
        
        # Generate LaTeX document
        latex = f"""\\documentclass[conference]{{IEEEtran}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{hyperref}}
\\usepackage{{cite}}
\\hypersetup{{
    colorlinks=true,
    linkcolor=blue,
    citecolor=blue,
    urlcolor=blue
}}
\\title{{{topic_escaped}}}

\\newcommand{{\\linebreakand}}{{
  \\end{{@IEEEauthorhalign}}
  \\hfill\\mbox{{}}\\par
  \\mbox{{}}\\hfill\\begin{{@IEEEauthorhalign}}
}}

\\author{{
{authors_text}
}}

\\begin{{document}}
\\maketitle

\\begin{{abstract}}
\\hspace{{}}{abstract_escaped}

\\end{{abstract}}

\\begin{{IEEEkeywords}}

\\end{{IEEEkeywords}}

\\section{{Introduction}}
\\hspace{{}}{introduction_escaped}

\\section{{Literature Review}}
\\hspace{{}}{literature_review_escaped}

\\section{{Methodology}}
\\hspace{{}}{methodology_escaped}

\\section{{Results}}


\\section{{Conclusion}}


{references}

\\end{{document}}
"""
        
        return latex
    
    @staticmethod
    def format_methodology_for_latex(methodology: str) -> str:
        """
        Format methodology text for LaTeX
        
        Args:
            methodology: Methodology text
            
        Returns:
            Formatted text with proper line breaks
        """
        # Replace newlines with double backslashes
        return methodology.replace("\n", "\\\\")

