import base64
import os
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import anthropic

load_dotenv()

app = FastAPI(title="Image Q&A API")
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}


@app.get("/")
def root():
    return {"status": "running", "message": "Image Q&A API"}


@app.post("/ask")
async def ask(
    file: UploadFile = File(...),
    question: str = Form(...),
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="JPG, PNG, GIF, WEBP만 지원합니다")

    image_bytes = await file.read()
    image_data = base64.standard_b64encode(image_bytes).decode("utf-8")

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {"type": "base64", "media_type": file.content_type, "data": image_data},
                    },
                    {"type": "text", "text": f"{question}\n\n한국어로 답변해주세요."},
                ],
            }
        ],
    )

    return JSONResponse(content={
        "question": question,
        "answer": message.content[0].text,
    })
