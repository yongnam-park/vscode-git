import pandas as pd
import os
from config import HISTORY_FILE

def load_history():
    """CSV 파일에서 데이터를 읽어와 리스트로 반환합니다."""
    if os.path.exists(HISTORY_FILE):
        try:
            return pd.read_csv(HISTORY_FILE).to_dict('records')
        except pd.errors.EmptyDataError:
            return []
        except Exception as e:
            print(f"로그 읽기 중 오류 발생: {e}")
            return []
    return []

def save_to_csv(data: dict):
    """데이터를 CSV 파일에 추가 저장합니다."""
    df_new = pd.DataFrame([data])
    header_needed = not os.path.exists(HISTORY_FILE)
    df_new.to_csv(HISTORY_FILE, mode='a', index=False, header=header_needed, encoding='utf-8-sig')

def delete_history():
    """저장된 파일을 물리적으로 삭제합니다."""
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)