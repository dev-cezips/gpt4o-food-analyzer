# 🍜 GPT-4o 음식 사진 분석기

AI에게 음식 사진을 보여주면,  
**무엇인지 추정하고 칼로리를 설명해주는** 감성 미니 앱입니다.

![preview](./screenshots/gpt4o-ramen-analysis-co
ver.jpg) <!-- 이미지 캡처 넣고 싶으면 여기에 저장 -->

---

## 📸 주요 기능

- 음식 사진을 업로드하면,
- GPT-4o가 어떤 음식인지 추정하고,
- 한식 위주의 설명과 칼로리 정보를 안내해줍니다.

---

## 🧠 사용 기술

| 기술 | 설명 |
|------|------|
| **Streamlit** | Python 기반 웹앱 프레임워크 |
| **OpenAI GPT-4o** | 이미지 + 텍스트를 함께 이해하는 멀티모달 AI |
| **Python-dotenv** | 환경변수로 API 키 안전하게 관리 |

---

## 🚀 실행 방법

```bash
git clone https://github.com/dev-cezips/gpt4o-food-analyzer.git
cd gpt4o-food-analyzer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # 환경변수 세팅
streamlit run app.py