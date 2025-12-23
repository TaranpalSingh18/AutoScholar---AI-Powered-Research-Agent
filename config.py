"""
Configuration file for Research Agent
"""
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Airtable Configuration
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY", "")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID", "appifFBfr2jFVP36T")
AIRTABLE_REFERENCE_TABLE_ID = os.getenv("AIRTABLE_REFERENCE_TABLE_ID", "tblIy3M8swS81a27j")
AIRTABLE_RESEARCH_TABLE_ID = os.getenv("AIRTABLE_RESEARCH_TABLE_ID", "tbl9nKld7ipICEMIj")

# GitHub Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_OWNER = os.getenv("GITHUB_OWNER", "Priyanshu314")
GITHUB_REPO = os.getenv("GITHUB_REPO", "research-work")

# OpenRouter Configuration (for citation)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Gmail Configuration (for human input)
GMAIL_CREDENTIALS = os.getenv("GMAIL_CREDENTIALS", "")

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# Authors Information
AUTHORS = [
    {
        "name": "Akshat Srivastava",
        "department": "Department of DSAI",
        "institution": "International Institute of Information Technology",
        "location": "Naya Raipur, Chhattisgarh",
        "email": "akshat22102@iiitnr.edu.in"
    },
    {
        "name": "Debashish Padhy",
        "department": "Department of DSAI",
        "institution": "International Institute of Information Technology",
        "location": "Naya Raipur, Chhattisgarh",
        "email": "debashish22102@iiitnr.edu.in"
    },
    {
        "name": "Priyanshu Srivastava",
        "department": "Department of DSAI",
        "institution": "International Institute of Information Technology",
        "location": "Naya Raipur, Chhattisgarh",
        "email": "priyanshu22101@iiitnr.edu.in"
    }
]

