"""
Simple script to run the research agent workflow
"""
import sys
from src.workflow import ResearchWorkflow

def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print("Usage: python run.py <topic> <description> [methodology_input]")
        print("Example: python run.py 'AI Ethics' 'Research on ethical implications of AI'")
        sys.exit(1)
    
    topic = sys.argv[1]
    description = sys.argv[2]
    methodology_input = sys.argv[3] if len(sys.argv) > 3 else None
    
    print(f"Starting research workflow for topic: {topic}")
    print(f"Description: {description}")
    print("-" * 50)
    
    workflow = ResearchWorkflow()
    result = workflow.execute(topic, description, methodology_input)
    
    if result.get("success"):
        print("\n✅ Workflow completed successfully!")
        print(f"\nAbstract:\n{result.get('abstract', '')[:200]}...")
        print(f"\nLaTeX document generated: {len(result.get('latex', ''))} characters")
        if result.get("github_url"):
            print(f"GitHub URL: {result.get('github_url')}")
        if result.get("flowchart_url"):
            print(f"Flowchart URL: {result.get('flowchart_url')}")
    else:
        print(f"\n❌ Workflow failed: {result.get('error', 'Unknown error')}")
        sys.exit(1)

if __name__ == "__main__":
    main()

