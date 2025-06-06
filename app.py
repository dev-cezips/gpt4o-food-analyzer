# 음식 사진 분석기 app.py

import streamlit as st
import openai
import os
import base64
from PIL import Image
import io  # Import io.BytesIO
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 페이지 레이아웃을 'centered'로 설정하여 다양한 화면 크기(모바일 포함)에서의 반응형 디자인을 개선합니다.
st.set_page_config(page_title="GPT-4o 음식 분석기", layout="centered")
st.title("🥢 음식 사진 분석기 with GPT-4o")
st.write("음식 사진을 업로드하면 GPT-4o가 어떤 음식인지 설명하고, 칼로리와 영양 정보를 예측해줘요.")

# 이미지 업로드
uploaded_file = st.file_uploader("📸 음식 사진 업로드", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file:
    # 이미지 보여주기 (원본 이미지 사용)
    # use_container_width=True는 이미지가 컨테이너 너비에 맞게 확장되도록 하여 모바일 장치에서 올바르게 스케일링됩니다.
    st.image(uploaded_file, caption="업로드한 음식", use_container_width=True)

    # --- API 전송용 이미지 리사이징 ---
    # 이미지가 특정 크기(max_size)를 초과하는 경우 리사이징합니다.
    # 이는 OpenAI API로 전송되는 데이터의 양을 줄여주며,
    # 특히 모바일 사용자의 데이터 사용량을 절약하고 분석 속도를 향상시킬 수 있습니다.
    # 사용자에게 표시되는 이미지는 st.image를 통해 원본으로 유지되어 시각적 품질을 보장합니다.
    # PIL을 사용하여 이미지 열기 및 리사이징
    img = Image.open(uploaded_file)
    max_size = 1024
    if img.width > max_size or img.height > max_size:
        img.thumbnail((max_size, max_size))

    # 리사이즈된 이미지를 바이트로 변환
    img_byte_arr = io.BytesIO()
    # 원본 포맷을 유지하려고 시도하되, 없으면 JPEG로 기본 설정
    img_format = img.format if img.format else 'JPEG'
    # RGBA 이미지를 RGB로 변환 (JPEG는 알파 채널을 지원하지 않음)
    if img_format == 'PNG' and img.mode == 'RGBA':
        img = img.convert('RGB')
    elif img_format == 'WEBP' and img.mode == 'RGBA': # WEBP도 RGBA 지원하지만, API 호환성을 위해 RGB로 변환 고려
        # 또는 img.save(img_byte_arr, format=img_format, save_all=True) 등으로 처리 가능
        # 여기서는 JPEG와 유사하게 RGB로 변환
        img = img.convert('RGB')


    img.save(img_byte_arr, format=img_format)
    image_bytes_for_api = img_byte_arr.getvalue()

    # 이미지 바이트를 base64로 인코딩
    base64_image = base64.b64encode(image_bytes_for_api).decode("utf-8")

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


