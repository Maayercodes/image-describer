import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set. Copy .env.example -> .env and add your key.")

genai.configure(api_key=API_KEY)

MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")

def call_vision_model_sync(image_bytes: bytes, instruction: str):
    """
    Synchronous wrapper that calls Gemini multimodal generate_content.
    Returns generated text (string) or raises RuntimeError.
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content([
            {"mime_type": "image/jpeg", "data": image_bytes},
            instruction
        ])
        return getattr(response, "text", str(response))
    except Exception as e:
        raise RuntimeError(f"Gemini call failed: {e}")
