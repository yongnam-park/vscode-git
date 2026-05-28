import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 내가 만든 logic.py에서 함수들을 불러옵니다.
from logic import simulate_lmea_analysis
from storage import load_history, save_to_csv, delete_history

def main():
    # 페이지 설정 및 제목
    st.set_page_config(
        page_title="LMEA Model Page", 
        page_icon="📺", 
        layout="centered",
        initial_sidebar_state="expanded"
    )

    # 초기 실행 시 파일에서 데이터 불러오기
    if "history" not in st.session_state:
        st.session_state.history = load_history()
    
    # 사이드바에 현재 상태 표시 (앱이 살아있는지 확인용)
    with st.sidebar:
        st.title("⚙️ 시스템 상태")
        st.success(f"엔진 가동 중")
        st.info(f"마지막 업데이트: {datetime.now().strftime('%H:%M:%S')}")
        if st.button("🔄 앱 강제 새로고침"):
            st.rerun()

    st.title("📺 LMEA Model Custom Page")
    st.markdown("---")
    st.subheader("Screen 사양 정보 입력")
    st.write("분석하거나 등록하고 싶은 Screen의 상세 정보를 아래에 입력해 주세요.")

    # 입력 폼 구성 - 데이터 입력을 그룹화하여 관리
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
        
        # UI와 분석 로직의 결합 (spinner는 UI에서 담당)
        with st.spinner('LMEA AI 모델이 사양을 분석 중입니다...'):
            analysis_score = simulate_lmea_analysis(screen_size, panel_type, resolution)
        
        # 데이터 저장
        new_data = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Size (inch)": screen_size,
            "Panel": panel_type,
            "Resolution": resolution,
            "Refresh (Hz)": refresh_rate,
            "Score": analysis_score
        }
        st.session_state.history.append(new_data)
        
        try:
            save_to_csv(new_data)
        except Exception as e:
            st.error(f"데이터 파일 저장 실패: {e}")
        
        st.success(f"✅ 분석이 완료되었습니다! (AI Score: {analysis_score})")
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric("분석 점수", f"{analysis_score} pts")
        with col_res2:
            st.info(f"""
            **주요 사양 요약:**
            - {screen_size}" {panel_type}
            - {resolution} @ {refresh_rate}Hz
            """)
        st.balloons()

    # 입력 이력 및 다운로드 섹션
    if st.session_state.history:
        st.markdown("---")
        st.subheader("📊 입력 이력 확인 및 내보내기")
        
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df, use_container_width=True)

        # 분석 점수 추이 시각화 추가
        if len(df) > 1:
            st.markdown("#### 📈 분석 점수 변동 추이")
            chart_df = df.copy()
            st.line_chart(chart_df.set_index("Timestamp")["Score"])

        col_dl, col_clr = st.columns([1, 1])
        with col_dl:
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 이력을 CSV로 다운로드",
                data=csv,
                file_name=f"lmea_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
            )
        with col_clr:
            if st.button("🗑️ 모든 이력 삭제", key="btn_clear_history"):
                delete_history()
                st.session_state.history = []
                st.rerun()

if __name__ == "__main__":
    main()
