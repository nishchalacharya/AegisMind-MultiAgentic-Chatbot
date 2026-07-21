# agents/voice.py
"""
Voice Agent - 100% FREE speech-to-text and text-to-speech
- Speech-to-Text: Whisper (local, offline)
- Text-to-Speech: gTTS (online, free, no API key)
"""

from pathlib import Path
from typing import Optional
import tempfile

class VoiceAgent:
    """
    Handles voice input (STT) and voice output (TTS)
    """
    
    def __init__(self, whisper_model_size: str = "base"):
        self.whisper_model_size = whisper_model_size
        self.whisper_model = None  # Lazy-loaded (only load when first used)
    
    def _load_whisper(self):
        """Load Whisper model lazily (only when actually needed)"""
        if self.whisper_model is None:
            import whisper
            print(f"📥 Loading Whisper '{self.whisper_model_size}' model...")
            self.whisper_model = whisper.load_model(self.whisper_model_size)
            print(f"✅ Whisper model loaded")
    
    def speech_to_text(self, audio_file_path: str) -> str:
        """
        Convert speech audio file to text using Whisper
        
        Args:
            audio_file_path: Path to audio file (mp3, wav, m4a, etc.)
        
        Returns:
            Transcribed text
        """
        self._load_whisper()
        
        audio_path = Path(audio_file_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
        
        print(f"🎤 Transcribing: {audio_path.name}")
        result = self.whisper_model.transcribe(str(audio_path))
        text = result["text"].strip()
        print(f"✅ Transcription: {text}")
        
        return text
    
    def text_to_speech(self, text: str, output_path: Optional[str] = None) -> str:
        """
        Convert text to speech audio file using gTTS
        
        Args:
            text: Text to convert
            output_path: Where to save the audio (optional, creates temp file if None)
        
        Returns:
            Path to the generated audio file
        """
        from gtts import gTTS
        
        if output_path is None:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            output_path = temp_file.name
            temp_file.close()
        
        print(f"🔊 Generating speech...")
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(output_path)
        print(f"✅ Audio saved: {output_path}")
        
        return output_path


# Test the voice agent
if __name__ == "__main__":
    agent = VoiceAgent()
    
    # Test 1: Text-to-Speech
    print("\n" + "="*50)
    print("TEST 1: Text-to-Speech")
    print("="*50)
    
    text = "Hello! This is AegisMind speaking through free, local voice tools."
    audio_file = agent.text_to_speech(text, output_path="data/test_output.mp3")
    print(f"Generated file: {audio_file}")
    
    # Test 2: Speech-to-Text (using the file we just created!)
    print("\n" + "="*50)
    print("TEST 2: Speech-to-Text (transcribing our own generated audio)")
    print("="*50)
    
    transcribed = agent.speech_to_text(audio_file)
    print(f"\nOriginal text: {text}")
    print(f"Transcribed:   {transcribed}")