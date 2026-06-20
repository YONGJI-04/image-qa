import os
import uuid
import base64
from typing import Literal
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

app = FastAPI(title="Image QA API", description="이미지에 대해 질문하면 Claude Vision이 답변합니다", version="1.1.0")

sessions: dict[str, dict] = {}

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}

@app.get("/")
def root():
    return {"status": "running", "message": "Image QA API - Claude Vision"}

@app.post("/ask")
async def ask(
    file: UploadFile = File(None),
    session_id: str = Form(None),
    question: str = Form(...),
    language: Literal["ko", "en"] = Form("ko"),
):
    lang_hint = "한국어로 답변해주세요." if language == "ko" else "Please answer in English."

    if file:
        if file.content_type not in ALLOWED_TYPES:
            raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다")
        contents = await file.read()
        b64 = base64.standard_b64encode(contents).decode("utf-8")
        new_session_id = uuid.uuid4().hex
        sessions[new_session_id] = {"image_b64": b64, "media_type": file.content_type, "history": []}
        session_id = new_session_id
    elif session_id and session_id in sessions:
        pass
    else:
        raise HTTPException(status_code=400, detail="이미지 파일 또는 유효한 session_id가 필요합니다")

    session = sessions[session_id]
    b64 = session["image_b64"]
    media_type = session["media_type"]

    messages = []
    if not session["history"]:
        messages.append({
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": b64}},
                {"type": "text", "text": f"{lang_hint}\n\n{question}"}
            ]
        })
    else:
        messages = session["history"].copy()
        messages.append({"role": "user", "content": question})

    response = client.messages.create(model="claude-sonnet-4-6", max_tokens=1024, messages=messages)
    answer = response.content[0].text

    session["history"].append({"role": "user", "content": question if session["history"] else f"{lang_hint}\n\n{question}"})
    session["history"].append({"role": "assistant", "content": answer})

    return {"session_id": session_id, "question": question, "answer": answer, "turn": len(session["history"]) // 2}

@app.delete("/session/{session_id}")
def clear_session(session_id: str):
    if session_id in sessions:
        del sessions[session_id]
        return {"message": "세션이 삭제되었습니다"}
    raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다")
