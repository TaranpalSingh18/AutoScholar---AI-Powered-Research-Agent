# AutoScholar - AI Research Agent 🚀

An AI-powered research paper generation system that automates the end-to-end academic research workflow. This Python implementation replicates the functionality of the n8n workflow defined in `research_agent.json`.

## Workflow Diagram

![Workflow](/assets/workflow.png)

## Features

- 📚 **ArXiv Integration**: Automatically fetches relevant research papers
- 🤖 **AI-Powered Writing**: Generates abstract, introduction, literature review, and methodology using OpenAI GPT
- 📝 **LaTeX Generation**: Creates IEEE-format research papers
- 📊 **Flowchart Generation**: Generates visual flowcharts from methodology using Graphviz
- 💾 **Airtable Integration**: Stores reference papers and research data
- 🔗 **GitHub Integration**: Automatically uploads generated papers to GitHub
- 📧 **Citation Management**: Automatically adds citations and formats references

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd autoscholar
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Configuration

Create a `.env` file with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key
AIRTABLE_API_KEY=your_airtable_api_key
GITHUB_TOKEN=your_github_token
OPENROUTER_API_KEY=your_openrouter_api_key  # Optional
```

## Usage

### API Server

Start the FastAPI server:

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Generate Research Paper

**Using the API:**

```bash
curl -X POST "http://localhost:8000/research" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "How ethical is AI",
    "description": "Give a short description of your research methodology"
  }'
```

**Using Python:**

```python
from src.workflow import ResearchWorkflow

workflow = ResearchWorkflow()
result = workflow.execute(
    topic="How ethical is AI",
    description="Research on AI ethics and implications"
)

print(result["abstract"])
print(result["latex"])
```

### Form Submission Endpoint

The `/research/form` endpoint accepts form data matching the n8n form trigger:

```bash
curl -X POST "http://localhost:8000/research/form?topic=AI%20Ethics&description=Research%20on%20AI%20ethics"
```

## Workflow Overview

The system follows this workflow (matching the n8n workflow):

1. **Form Submission**: Receives research topic and description
2. **ArXiv Fetch**: Fetches 5 relevant papers from arXiv
3. **Data Processing**: Extracts and formats paper data
4. **Airtable Storage**: Stores reference papers
5. **AI Generation**:
   - Abstract Writer
   - Introduction Writer
   - Literature Reviewer
   - Reference Agent
   - Citation Agent
   - Methodology Agent
   - Flowchart Agent
6. **LaTeX Generation**: Creates IEEE-format document
7. **GitHub Upload**: Uploads LaTeX file to repository

## Project Structure

```
.
├── main.py                 # FastAPI server
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── src/
│   ├── __init__.py
│   ├── arxiv_fetcher.py    # ArXiv paper fetching
│   ├── ai_agents.py        # AI agents (Abstract, Introduction, etc.)
│   ├── airtable_client.py  # Airtable integration
│   ├── github_client.py    # GitHub integration
│   ├── latex_generator.py # LaTeX document generation
│   ├── citation_processor.py # Citation processing
│   ├── flowchart_generator.py # Flowchart generation
│   └── workflow.py         # Main workflow orchestrator
└── research_agent/
    └── research_agent.json # Original n8n workflow definition
```

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /research` - Generate research paper (JSON body)
- `POST /research/form` - Form submission endpoint (query parameters)

## Dependencies

- **FastAPI**: Web framework
- **OpenAI**: AI text generation
- **PyAirtable**: Airtable integration
- **PyGithub**: GitHub integration
- **xmltodict**: XML parsing for ArXiv
- **requests**: HTTP requests

## Notes

- The system requires API keys for OpenAI, Airtable, and GitHub
- Airtable base and table IDs are configured in `config.py`
- GitHub repository must exist before uploading files
- Flowchart generation uses QuickChart.io Graphviz service

## License

MIT License

