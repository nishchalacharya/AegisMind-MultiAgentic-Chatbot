"""
Main entry point for AegisMind
"""

from aegismind.ui.cli import main as cli_main
from aegismind.config.settings import get_settings
import sys 

def main():
    """Initialize and run AegisMind"""
    # Load settings  ( validates env vars )
    try:
        settings = get_settings()
        print(f"Loaded settings.Using model: {settings.groq_model}")
    except Exception as e:
        print(f"Configuration error: {str(e)}")
        print("\nMake sure you have a .env file with:")
        print("GROQ_API_KEY=your_api_key_here")
        sys.exit(1)
        
    
    # Launch CLI 
    cli_main()    
    

if __name__ == "__main__":
    main()        
    