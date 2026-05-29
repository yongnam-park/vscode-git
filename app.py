import streamlit as st
import pandas as pd

def main():
    # 1. 페이지 기본 설정
    st.set_page_config(
        page_title="New Service Project",
        page_icon="🚀",
        layout="wide"
    )

    # 2. 헤더 섹션
    st.title("🚀 새로운 프로젝트 시작")
    st.info("이 프로젝트는 기존 튜토리얼과 완전히 분리된 신규 서비스입니다.")

    # 3. 사이드바 - 설정이나 필터링 배치 예정
    with st.sidebar:
        st.header("Project Settings")
        st.write("새로운 환경에서 설정을 구성하세요.")

    st.write("여기에 새로운 로직을 구현하면 됩니다.")

if __name__ == "__main__":
    main()