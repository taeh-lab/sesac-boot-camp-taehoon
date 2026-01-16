
import json
import os
import sys

# 설정 파일이 저장될 디렉터리 경로
# 사용자의 홈 디렉터리 밑에 MorningBooster 폴더를 생성합니다.
CONFIG_DIR = os.path.join(os.path.expanduser("~"), "MorningBooster")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

def get_default_config():
    """기본 설정값을 반환합니다."""
    return {
        "chrome_path": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "windows": [
            {
                "name": "AI 창",
                "urls": ["https://gemini.google.com/", "https://chatgpt.com/"]
            },
            {
                "name": "업무 창",
                "urls": ["https://www.notion.so/", "https://github.com/"]
            }
        ],
        "apps": [
            {"name": "카카오톡", "path": r"C:\Program Files (x86)\Kakao\KakaoTalk\KakaoTalk.exe"},
            {"name": "디스코드", "path": r"C:\Users\tahoon\AppData\Local\Discord\Update.exe"}
        ]
    }

def load_config():
    """설정 파일을 읽어오거나, 없으면 기본값으로 새로 생성합니다."""
    # 설정 폴더가 없으면 생성
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
        
    if not os.path.exists(CONFIG_PATH):
        config = get_default_config()
        save_config(config)
        return config
    
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # 파일이 손상되었거나 비어있는 경우, 기본 설정으로 덮어씁니다.
        config = get_default_config()
        save_config(config)
        return config

def save_config(config):
    """설정 내용을 JSON 파일에 저장합니다."""
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"설정 저장 중 오류 발생: {e}")
        return False

def get_resource_path(relative_path):
    """ PyInstaller로 패키징되었을 때의 리소스 경로를 반환합니다. """
    try:
        # PyInstaller가 생성한 임시 폴더
        base_path = sys._MEIPASS
    except Exception:
        # 일반적인 Python 환경
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
