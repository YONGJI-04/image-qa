# Image Q&A

이미지를 업로드하고 질문하면 Claude Vision이 답변해주는 API

## 아키텍처

```
이미지 파일 + 질문 텍스트
        ↓
Claude Vision (claude-sonnet-4-6)
        ↓
질문에 대한 답변 반환 (한국어)
```

## 활용 예시

- "이 음식의 칼로리는 얼마나 될까요?"
- "이 건물은 어느 나라 양식인가요?"
- "이 차트에서 가장 높은 값은 무엇인가요?"
- "이 식물의 이름은 무엇인가요?"

## API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/` | 서버 상태 확인 |
| POST | `/ask` | 이미지 + 질문 → 답변 |
| GET | `/docs` | Swagger UI |

## 요청 예시

```bash
curl -X POST http://localhost:8000/ask \
  -F "file=@photo.jpg" \
  -F "question=이 이미지에서 무엇이 보이나요?"
```

## 응답 예시

```json
{
  "question": "이 이미지에서 무엇이 보이나요?",
  "answer": "이미지에는 ..."
}
```

## 실행 방법

```bash
cp .env.example .env
pip install -r requirements.txt
cd app && uvicorn main:app --host 0.0.0.0 --port 8002
```

## 환경 변수

```
ANTHROPIC_API_KEY=   # Anthropic Claude API 키
```
