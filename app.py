# 음식 사진 분석기 app.py

import streamlit as st
import openai
import os
import base64
from PIL import Image
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="GPT-4o 음식 분석기", layout="centered")
st.title("🥢 음식 사진 분석기 with GPT-4o")
st.write("음식 사진을 업로드하면 GPT-4o가 어떤 음식인지 설명하고, 칼로리와 영양 정보를 예측해줘요.")

# 업로드된 이미지 base64로 인코딩
def encode_image_to_base64(image_file):
    image_bytes = image_file.read()
    return base64.b64encode(image_bytes).decode("utf-8")

# 이미지 업로드
uploaded_file = st.file_uploader("📸 음식 사진 업로드", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file:
    # 이미지 보여주기
    st.image(uploaded_file, caption="업로드한 음식", use_container_width=True)

    # 이미지 base64 인코딩
    base64_image = encode_image_to_base64(uploaded_file)

    # GPT-4o에게 메시지 구성
    messages=[
        {
            "role": "system", 
            "content": "당신은 음식 전문가이며, 음식 이미지를 보고 어떤 음식인지 분석한 후 칼로리와 주요 영양 정보를 예측해줍니다. 친근하고 쉬운 말투를 사용하세요."
        },
        {
            "role": "user", 
            "content": [
                {"type": "text", "text": "이 음식이 뭔지 알려줘. 한국 음식 위주로 추정해줘. 간단한 칼로리 예측도 부탁해."},
                {"type": "image_url","image_url": {"url": f"data:image/jpeg;base64, {base64_image}"}}
            ]
        }
    ]

    with st.spinner("GPT-4o가 이미지를 분석 중입니다.... 🍜"):
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=500
            )
            gpt_reply = response.choices[0].message.content

            st.markdown("---")
            st.subheader("🍛 GPT-4o 분석 결과")
            st.write(gpt_reply)

        except openai.OpenAIError as e:
            st.error(f"‼️ 오류가 발생했어여. {e}")


