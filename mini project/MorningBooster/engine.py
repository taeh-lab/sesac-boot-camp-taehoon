
import subprocess
import time
import os
import webbrowser # 웹브라우저를 열기 위한 모듈 추가

def _open_browser_window(chrome_path, urls):
    """하나의 새 크롬 창에 여러 URL을 엽니다."""
    if not urls:
        return
    try:
        args = [chrome_path, "--new-window"] + urls
        subprocess.Popen(args)
        time.sleep(1)  # 창이 안정적으로 열리도록 잠시 대기
    except FileNotFoundError:
        print(f"오류: 크롬 경로를 찾을 수 없습니다 - '{chrome_path}'")
    except Exception as e:
        print(f"브라우저 실행 중 오류 발생: {e}")

def start_environment(config):
    """설정값에 따라 전체 환경을 실행합니다."""
    print("MorningBooster 실행 시작...")
    chrome_path = config.get("chrome_path")

    if not chrome_path or not os.path.exists(chrome_path):
        print(f"오류: 설정된 크롬 경로가 유효하지 않습니다 - '{chrome_path}'")
        return False

    # 1. 지정된 브라우저 창들 열기
    windows = config.get("windows", [])
    for i, window_group in enumerate(windows, 1):
        urls = window_group.get("urls", [])
        print(f"{i}번 창 그룹 실행 중...")
        _open_browser_window(chrome_path, urls)

    # 2. 지정된 로컬 프로그램들 실행
    apps = config.get("apps", [])
    print("로컬 프로그램 실행 중...")
    for app in apps:
        app_path = app.get("path")
        app_name = app.get("name", "알 수 없는 프로그램")
        if app_path and os.path.exists(app_path):
            try:
                subprocess.Popen([app_path])
                print(f"- {app_name} 실행 완료.")
            except Exception as e:
                print(f"오류: {app_name} 실행 실패 - {e}")
        else:
            print(f"- {app_name} 경로가 설정되지 않았거나 잘못되었습니다. 건너뜁니다.")
    
    # 3. 개발자님의 잠금 링크 열기 (모든 작업 완료 후)
    # --- 이 부분에 나중에 티스토리 블로그 URL을 넣어주세요! ---
    TISTORY_URL = "https://sceen.tistory.com/5" # <<<<< 여기에 URL을 넣어주세요!
    # --------------------------------------------------------
    # 조건문 수정: 플레이스홀더 문자열이 아니고 비어있지 않을 때만 실행
    if TISTORY_URL and TISTORY_URL != "YOUR_TISTORY_BLOG_URL_HERE": 
        try:
            print(f"개발자님의 티스토리 블로그를 엽니다: {TISTORY_URL}")
            webbrowser.open(TISTORY_URL)
        except Exception as e:
            print(f"오류: 티스토리 블로그를 여는 데 실패했습니다 - {e}")
    else:
        print("티스토리 블로그 URL이 설정되지 않았거나 유효하지 않습니다. 잠금 링크를 건너뜁니다.")

    print("MorningBooster 실행 완료.")
    return True
