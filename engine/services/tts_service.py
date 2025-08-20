# engine/services/tts.py
from gtts import gTTS
from pathlib import Path


class TTSService:
    def __init__(self, output_dir: str = "engine/temp_audio"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def text_to_speech(self, text: str, filename: str = None) -> str:
        if filename is None:
            filename = f"tts_{abs(hash(text))}.mp3"
        file_path = self.output_dir / filename

        # Generate audio using gTTS
        tts = gTTS(text=text, lang="en")
        tts.save(str(file_path))

        return str(file_path)
