from pathlib import Path
import wave
from piper.voice import PiperVoice

def text_to_speech(text: str, output_path: str = None) -> dict:
    try:
        if not text or len(text.strip()) == 0:
            return {
                "success": False,
                "audio_path": None,
                "audio_bytes": None,
                "error": "Empty text"
            }
        if output_path is None:
            import time
            output_path = f"output_speech/speech_{int(time.time())}.wav"
        output_path = Path(output_path) # set where to save the audio 
        output_path.parent.mkdir(parents=True, exist_ok=True)

        model_path = Path("src/en_US-lessac-medium.onnx")
        voice = PiperVoice.load(str(model_path)) # Load the voice

        with wave.open(str(output_path), "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(voice.config.sample_rate)
            voice.synthesize_wav(text, wav_file)

        with open(output_path, "rb") as f:
            audio_bytes = f.read()

        return {
            "success": True,
            "audio_path": str(output_path),
            "audio_bytes": audio_bytes,
            "error": None,
        }
    except Exception as e:
        return {
            "success": False,
            "audio_path": None,
            "audio_bytes": None,
            "error": e
        }