import time
from config import BASE_SCORE_OLED, BASE_SCORE_LCD, LARGE_SCREEN_BONUS, SIZE_THRESHOLD

# 패널별 기본 점수를 딕셔너리로 관리 (나중에 추가하기 쉬움)
PANEL_SCORES = {
    "OLED": BASE_SCORE_OLED,
    "LCD": BASE_SCORE_LCD,
    "Micro LED": 95.0,
    "Mini LED": 88.0
}

RESOLUTION_BONUS = {
    "UHD/4K (3840x2160)": 5.0,
    "8K": 10.0,
    "QHD (2560x1440)": 2.0
}

def simulate_lmea_analysis(size: float, panel: str, resolution: str) -> float:
    """입력된 사양을 기반으로 가상의 LMEA 분석 결과를 생성합니다."""
    time.sleep(1.0) # 분석 시뮬레이션
    
    # 1. 패널별 기본 점수 설정 (딕셔너리 활용)
    score = PANEL_SCORES.get(panel, BASE_SCORE_LCD)
    
    # 2. 화면 크기에 따른 보너스 점수
    if size > SIZE_THRESHOLD:
        score += LARGE_SCREEN_BONUS

    # 3. 해상도에 따른 보너스 점수 추가
    score += RESOLUTION_BONUS.get(resolution, 0.0)
    
    return round(score, 1)
# ... (위에는 함수 정의들)

if __name__ == "__main__":
    # 1. 터미널에서 'python logic.py'라고 치면 이 안의 코드가 실행됩니다.
    # 2. 하지만 app.py에서 'from logic import ...'를 하면 이 안은 무시됩니다.
    print("--- Logic Module Test ---")
    test_score = simulate_lmea_analysis(55.0, "OLED", "UHD/4K")
    print(f"Test Result (55 inch, OLED): {test_score} pts")
