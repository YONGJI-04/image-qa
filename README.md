# Image Q&A

이미지를 업로드하고 자유롭게 질문하면 **Claude Vision**이 이미지를 보고 답변해주는 시각 질의응답 API

---

## 프로젝트 개요

단순한 이미지 설명을 넘어, 사용자가 원하는 것을 직접 물어볼 수 있습니다. 음식 칼로리 추정, 건물 양식 분석, 차트 해석, 식물 이름 식별 등 이미지에 관한 어떤 질문도 가능합니다.

---

## 아키텍처

```
이미지 파일 + 자유 형식 질문 텍스트
            ↓
    Base64 인코딩
            ↓
    [ Claude Vision API ]
    claude-sonnet-4-6
    이미지 + 질문 동시 처리
            ↓
    한국어 답변 반환
```

---

## 사용 기술 스택

| 기술 | 역할 |
|------|------|
| **Claude Vision** (claude-sonnet-4-6) | 이미지 기반 질의응답 |
| **FastAPI** | REST API 서버 (multipart/form-data 처리) |

---

## 활용 예시

| 이미지 | 질문 예시 |
|--------|-----------|
| 음식 사진 | "이 음식의 예상 칼로리는?" |
| 건축물 사진 | "어느 나라 건축 양식인가요?" |
| 데이터 차트 | "가장 높은 값은 언제인가요?" |
| 식물 사진 | "이 식물의 이름과 특징은?" |
| 제품 사진 | "이 제품의 브랜드를 알 수 있나요?" |
| 지도 | "이 지역은 어디인가요?" |

---

## 디렉토리 구조

```
image-qa/
├── app/
│   └── main.py   # FastAPI 서버 + Claude Vision Q&A 로직
├── requirements.txt
├── .env.example
└── README.md
```

---

## API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| `GET` | `/` | 서버 상태 확인 |
| `POST` | `/ask` | 이미지 + 질문 → 답변 |
| `GET` | `/docs` | Swagger UI |

---

## 요청 / 응답 예시

```bash
curl -X POST http://localhost:8000/ask \
  -F "file=@food.jpg" \
  -F "question=이 음식의 예상 칼로리는 얼마인가요?"
```

**응답:**

```json
{
  "question": "이 음식의 예상 칼로리는 얼마인가요?",
  "answer": "이미지에 보이는 음식은 김치찌개로 보입니다. 일반적인 1인분 기준으로 약 200-300kcal 정도로 추정됩니다. 두부와 돼지고기가 포함된 경우 단백질 함량이 높고..."
}
```

---

## 지원 형식

- **파일 형식**: JPG, PNG, GIF, WEBP
- **질문 언어**: 한국어/영어 모두 가능
- **답변 언어**: 한국어 (고정)

---

## 실행 방법

```bash
cp .env.example .env
pip install -r requirements.txt
cd app && uvicorn main:app --host 0.0.0.0 --port 8002
```

## 환경 변수

| 변수 | 설명 |
|------|------|
| `ANTHROPIC_API_KEY` | Anthropic Claude API 키 |
