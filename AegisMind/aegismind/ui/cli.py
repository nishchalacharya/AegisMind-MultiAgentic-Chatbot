# aegismind/ui/cli.py

#  feature 5 
"""
Command-line interface for AegisMind
"""

import click 
from rich.console import Console 
from rich.panel import Panel 
from rich.markdown import Markdown 
from orchestration.graph import AgentOrchestrator

console=Console()

class AegisMindCLI:
    """Interactive CLI for AegisMind"""
    
    def __init__(self):
        self.orchestrator= AgentOrchestrator()
        self.user_id = "cli_user" # In a real app, this would be dynamic
        
    
    def run(self):
        """start interactive chat sessions"""
        console.print(Panel.fit(
            "[bold cyan]AegisMind[/bold cyan] - Agentic AI System\n"
            "Type your message or 'quit' to exit",
            border_style="cyan"
        ))    
        
        
        while True:
            try:
                # Get user input 
                user_input =console.input("\n[bold green]You:[/bold green] ")
                
                if user_input.lower() in ['quit','exit','q']:
                    console.print("[yellow]Goodbye! 👋[/yellow]")
                    break 
                
                if not user_input.strip():
                    continue
                
                # Process through orchestrator
                response =self.orchestrator.run(
                    user_message=user_input,
                    user_id= self.user_id
                    
                )
                
                # Display response 
                console.print(f"\n[bold blue]AegisMind:[/bold blue] {response}")
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Goodbye! 👋[/yellow]")
                break 
            
            except Exception as e:
                console.print(f"[red]Error:[/red] {str(e)}")
                
                
                
@click.command()
def main():
    """Launch AegisMind CLI"""
    cli=AegisMindCLI()
    cli.run()
    
    
if __name__ == "__main__":
    main()
        
                    
        
        