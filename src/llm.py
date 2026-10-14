import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def generate_llm_response(user_text: str) -> dict:
    try:
        client = Groq(api_key = os.getenv("GROQ_API_KEY"))
        
        # --- SYSTEM PROMPT PLACEHOLDER ---
        # Later, we will inject custom instructions here to detect 
        # physical commands like "move forward"
        system_prompt = (
            "You are the brain of an empathetic emotional support humanoid robot. "
            "Your responses should be warm, concise, supportive, and natural for speech. "
            "Keep answers relatively short (1-3 sentences) so the text-to-speech doesn't take too long."
        )
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        response_text = completion.choices[0].message.content.strip()
        
        return {
            "success": True,
            "text": response_text,
            "error": None
        }
        
    except Exception as e:
        print(f"LLM Error: {e}")
        return {
            "success": False,
            "text": "",
            "error": str(e)
        }