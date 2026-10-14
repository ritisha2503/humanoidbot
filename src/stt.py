from faster_whisper import WhisperModel

def speech_to_text(audio_path: str) -> dict:
    try:
        model = WhisperModel("base", device="cpu", compute_type="int8") # load the model
        segments, info = model.transcribe(audio_path, language="en") # convert audio to text
        text = "".join(segment.text for segment in segments).strip() # combine all parts into a single string

        if not text:
            return {
                "success": False,
                "text": "",
                "error": "No speech detected"
            }
        
        return {
            "success": True,
            "text": text,
            "error": None,
        }
    except Exception as e:
        print(f"Encountered error: {e}")
        return {
            "success": False,
            "text": "",
            "error": e
        }