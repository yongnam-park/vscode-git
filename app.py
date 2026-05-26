import streamlit as st

def main():
    # 페이지 설정 및 제목
    st.set_page_config(page_title="LMEA Model Page", page_icon="📺", layout="centered")
    
    st.title("📺 LMEA Model Custom Page")
    st.markdown("---")
    st.subheader("Screen 사양 정보 입력")
    st.write("분석하거나 등록하고 싶은 Screen의 상세 정보를 아래에 입력해 주세요.")

    # 입력 폼 구성
    with st.form("screen_info_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            screen_size = st.number_input("화면 크기 (inch)", min_value=10.0, max_value=150.0, value=32.0, step=0.1)
            resolution = st.selectbox("해상도", ["FHD (1920x1080)", "QHD (2560x1440)", "UHD/4K (3840x2160)", "8K", "기타"])
            
        with col2:
            panel_type = st.radio("패널 종류", ["OLED", "LCD", "Micro LED", "Mini LED"])
            refresh_rate = st.slider("주사율 (Hz)", 60, 360, 144)

        additional_specs = st.text_area("기타 추가 사양 정보", placeholder="예: HDR10 지원, 응답속도 1ms 등")
        
        # 제출 버튼
        submit_button = st.form_submit_button(label="정보 제출 및 분석 요청")

    # 결과 출력
    if submit_button:
        st.success("✅ 정보가 성공적으로 입력되었습니다!")
        st.info(f"""
        **입력된 요약 정보:**
        - 크기/패널: {screen_size}인치 {panel_type}
        - 해상도/주사율: {resolution} / {refresh_rate}Hz
        - 기타 사양: {additional_specs if additional_specs else '없음'}
        """)
        st.balloons()

if __name__ == "__main__":
    main()
