# image-qa

이미지 업로드 + 질문 → Claude Vision 답변

## 실행 방법

```bash
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API 문서

서버 실행 후 http://localhost:8000/docs 접속
