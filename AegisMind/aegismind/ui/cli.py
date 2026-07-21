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
from agents.voice import VoiceAgent

console=Console()

class AegisMindCLI:
    """Interactive CLI for AegisMind"""
    
    def __init__(self,voice_enabled:bool = False):
        self.orchestrator= AgentOrchestrator()
        self.user_id = "cli_user" # In a real app, this would be dynamic
        self.voice_enabled =  voice_enabled
        self.voice_agent=None

        if self.voice_enabled:
            self.voice_agent =  VoiceAgent()

        
    
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
                
                # Voice output (if enabled)
                if self.voice_enabled and self.voice_agent:
                    try:
                        audio_path = self.voice_agent.text_to_speech(
                            response,
                            output_path="data/voice_output.mp3"
                        )
                        console.print(
                            f"[dim]🔊 Voice saved to: {audio_path} "
                            f"(open this file on your host machine to listen)[/dim]"
                        )
                    except Exception as e:
                        console.print(f"[red]Voice generation failed: {e}[/red]")
                
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Goodbye! 👋[/yellow]")
                break 
            
            except Exception as e:
                console.print(f"[red]Error:[/red] {str(e)}")
                
                
                
@click.command()
@click.option('--voice',is_flag=True,help='Enable voice output (TTS)')
def main(voice):
    """Launch AegisMind CLI"""
    cli=AegisMindCLI(voice_enabled=voice)
    cli.run()
    
    
if __name__ == "__main__":
    main()
        
                    
        
        