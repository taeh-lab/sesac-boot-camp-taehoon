
import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk
import threading
import engine # 실제 작업을 수행할 엔진 모듈

class LoadingScreen(tk.Toplevel):
    """
    작업 실행 중 보여질 로딩 화면.
    GUI가 멈추는 것을 방지하기 위해 별도의 스레드에서 작업을 실행합니다.
    """
    def __init__(self, parent, image_path, config):
        super().__init__(parent)

        self.config = config
        
        # --- 창 설정 ---
        self.overrideredirect(True) # 타이틀 바 제거
        self.attributes("-topmost", True) # 항상 위에 표시

        # --- 위젯 생성 ---
        self.label_font = font.Font(family="Helvetica", size=12)
        
        # 이미지 표시
        try:
            pil_image = Image.open(image_path)
            # 이미지가 너무 크면 리사이즈 (예: 300x300)
            pil_image.thumbnail((300, 300))
            self.bear_image = ImageTk.PhotoImage(pil_image)
            self.image_label = ttk.Label(self, image=self.bear_image)
            self.image_label.pack(pady=(20, 10))
        except FileNotFoundError:
            self.image_label = ttk.Label(self, text="이미지 없음", font=self.label_font)
            self.image_label.pack(pady=(20, 10), padx=50)

        # 메시지 레이블
        self.message_label = ttk.Label(self, text="MorningBooster를 준비 중입니다...", font=self.label_font)
        self.message_label.pack(pady=10)

        # 프로그레스 바 (회전 스피너)
        self.progress = ttk.Progressbar(self, mode='indeterminate', length=250)
        self.progress.pack(pady=10, padx=20)
        
        self.update_idletasks() # 위젯 사이즈 계산

        # --- 창 위치 중앙 정렬 ---
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        win_width = self.winfo_width()
        win_height = self.winfo_height()

        x = parent_x + (parent_width - win_width) // 2
        y = parent_y + (parent_height - win_height) // 2
        self.geometry(f'{win_width}x{win_height}+{x}+{y}')

        # --- 작업 시작 ---
        self.run_task()

    def run_task(self):
        """프로그레스 바를 활성화하고 백그라운드에서 작업을 시작합니다."""
        self.progress.start(10)
        self.task_thread = threading.Thread(target=self._task_runner)
        self.task_thread.start()

    def _task_runner(self):
        """백그라운드 스레드에서 실행될 작업."""
        engine.start_environment(self.config)
        
        # 작업 완료 후, 메인 스레드에서 GUI 업데이트를 예약
        self.after(0, self._on_task_complete)

    def _on_task_complete(self):
        """작업 완료 시 호출될 메소드 (메인 스레드)."""
        self.progress.stop()
        self.message_label.config(text="✨ 즐거운 하루 되세요! ✨")
        
        # 2초 후에 창을 자동으로 닫음
        self.after(2000, self.destroy)
