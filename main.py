from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from model_client import call_vision_model_sync
from PIL import Image
import io

app = FastAPI(title="Gemini Image Describer")

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# Describe single image
@app.post("/describe")
async def describe(
    file: UploadFile,
    instruction: str = Form(...),
    tone: str = Form("Friendly"),
    length: str = Form("Medium"),
):
    try:
        contents = await file.read()
        # Verify image
        try:
            Image.open(io.BytesIO(contents))
        except:
            return JSONResponse({"error": "Uploaded file is not a valid image."}, status_code=400)
        
        # Build prompt dynamically
        prompt = f"{instruction}\nTone: {tone}\nLength: {length}"
        
        # Call Gemini
        description = call_vision_model_sync(contents, prompt)
        return {"description": description}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
