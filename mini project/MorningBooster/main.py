import tkinter as tk
from tkinter import ttk, messagebox, font
import os
import webbrowser

# 다른 모듈에서 기능 가져오기
import storage
from loading_screen import LoadingScreen # 새로 만든 로딩스크린 모듈

class SettingsWindow(tk.Toplevel):
    """설정 창을 관리하는 클래스"""
    def __init__(self, parent):
        super().__init__(parent)
        self.transient(parent)
        self.grab_set()
        self.title("설정")
        self.geometry("650x780")
        self.resizable(False, False)

        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        self.general_font = ('Malgun Gothic', 10)
        self.button_font = ('Malgun Gothic', 10, 'bold')
        self.label_frame_font = ('Malgun Gothic', 11, 'bold')

        self.style.configure("TLabel", font=self.general_font)
        self.style.configure("TButton", font=self.button_font, padding=6)
        self.style.configure("TEntry", font=self.general_font, padding=3)
        self.style.configure("TLabelframe.Label", font=self.label_frame_font, foreground="#333333")
        self.style.configure("TLabelframe", padding=10)

        self.config = storage.load_config()
        self.widgets = {}

        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas = tk.Canvas(main_frame, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=620)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._create_widgets()

    def _on_close(self):
        self.destroy()

    def _create_widgets(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        chrome_frame = ttk.LabelFrame(self.scrollable_frame, text="Chrome 경로")
        chrome_frame.pack(padx=5, pady=8, fill="x")
        self.widgets['chrome_path_entry'] = ttk.Entry(chrome_frame)
        self.widgets['chrome_path_entry'].insert(0, self.config.get("chrome_path", ""))
        self.widgets['chrome_path_entry'].pack(padx=5, pady=5, fill="x", expand=True)

        self.widgets['window_entries'] = []
        windows_frame = ttk.LabelFrame(self.scrollable_frame, text="브라우저 창 그룹 (최대 4개)")
        windows_frame.pack(padx=5, pady=8, fill="x")

        for i, window_group in enumerate(self.config.get("windows", [])):
            window_group_frame = ttk.Frame(windows_frame, padding=8, relief="solid", borderwidth=1)
            window_group_frame.pack(padx=5, pady=5, fill="x")
            
            title_row_frame = ttk.Frame(window_group_frame)
            title_row_frame.pack(fill="x", expand=True, pady=(0,5))
            
            group_name_entry = ttk.Entry(title_row_frame, width=15, font=self.button_font)
            group_name_entry.insert(0, window_group.get("name", f"{i+1}번 창"))
            group_name_entry.pack(side="left", padx=5, pady=2)
            
            ttk.Button(title_row_frame, text="X 창 삭제", command=lambda idx=i: self._delete_window(idx), style="Danger.TButton").pack(side="right")
            
            urls_entries = []
            for j, url in enumerate(window_group.get("urls", [])):
                url_row_frame = ttk.Frame(window_group_frame)
                url_row_frame.pack(fill="x", padx=5, pady=2)
                entry = ttk.Entry(url_row_frame)
                entry.insert(0, url)
                entry.pack(side="left", expand=True, fill="x", padx=(0,5))
                ttk.Button(url_row_frame, text="X", width=3, command=lambda w_idx=i, u_idx=j: self._delete_url(w_idx, u_idx), style="Danger.TButton").pack(side="left")
                urls_entries.append(entry)
            
            if len(window_group.get("urls", [])) < 4:
                ttk.Button(window_group_frame, text="+ 링크 추가", command=lambda idx=i: self._add_url(idx), style="Accent.TButton").pack(pady=5, padx=5, anchor="w")
            
            self.widgets['window_entries'].append({'name': group_name_entry, 'urls': urls_entries})

        if len(self.config.get("windows", [])) < 4:
            ttk.Button(windows_frame, text="+ 새 창 추가", command=self._add_window, style="Accent.TButton").pack(pady=10)

        self.widgets['app_entries'] = []
        apps_frame = ttk.LabelFrame(self.scrollable_frame, text="로컬 프로그램")
        apps_frame.pack(padx=5, pady=8, fill="x")

        for i, app in enumerate(self.config.get("apps", [])):
            app_row_frame = ttk.Frame(apps_frame, padding=5, relief="solid", borderwidth=1)
            app_row_frame.pack(fill="x", padx=5, pady=5)
            
            name_entry = ttk.Entry(app_row_frame, width=15)
            name_entry.insert(0, app.get("name", ""))
            name_entry.pack(side="left", padx=5)

            path_entry = ttk.Entry(app_row_frame)
            path_entry.insert(0, app.get("path", ""))
            path_entry.pack(side="left", expand=True, fill="x", padx=(0,5))

            ttk.Button(app_row_frame, text="X", width=3, command=lambda idx=i: self._delete_app(idx), style="Danger.TButton").pack(side="left")
            self.widgets['app_entries'].append({'name': name_entry, 'path': path_entry})

        ttk.Button(apps_frame, text="+ 프로그램 추가", command=self._add_app, style="Accent.TButton").pack(pady=10)

        save_button = ttk.Button(self.scrollable_frame, text="저장 후 닫기", command=self._save_and_close, style="Primary.TButton")
        save_button.pack(pady=20)

        self.style.configure("Primary.TButton", background="#4CAF50", foreground="white", font=self.button_font)
        self.style.map("Primary.TButton", background=[('active', '#4CAF50')])
        self.style.configure("Accent.TButton", background="#2196F3", foreground="white", font=self.button_font)
        self.style.map("Accent.TButton", background=[('active', '#2196F3')])
        self.style.configure("Danger.TButton", background="#F44336", foreground="white", font=self.button_font)
        self.style.map("Danger.TButton", background=[('active', '#F44336')])

    def _add_window(self):
        if len(self.config.get("windows", [])) < 4:
            self.config.get("windows", []).append({"name": "새 창", "urls": [""]})
            self._create_widgets()

    def _delete_window(self, index):
        self.config.get("windows", []).pop(index)
        self._create_widgets()

    def _add_url(self, window_index):
        if len(self.config.get("windows", [])[window_index].get("urls", [])) < 4:
            self.config.get("windows", [])[window_index].get("urls", []).append("")
            self._create_widgets()
            
    def _delete_url(self, window_index, url_index):
        self.config.get("windows", [])[window_index].get("urls", []).pop(url_index)
        self._create_widgets()
        
    def _add_app(self):
        self.config.get("apps", []).append({"name": "", "path": ""})
        self._create_widgets()

    def _delete_app(self, index):
        self.config.get("apps", []).pop(index)
        self._create_widgets()

    def _save_and_close(self):
        self.config['chrome_path'] = self.widgets['chrome_path_entry'].get()
        
        new_windows = []
        for window_widget_group in self.widgets['window_entries']:
            urls = [url_entry.get() for url_entry in window_widget_group['urls'] if url_entry.get()]
            if urls:
                new_windows.append({
                    "name": window_widget_group['name'].get(),
                    "urls": urls
                })
        self.config['windows'] = new_windows

        new_apps = []
        for app_widget_group in self.widgets['app_entries']:
            if app_widget_group['name'].get() and app_widget_group['path'].get():
                 new_apps.append({
                    "name": app_widget_group['name'].get(),
                    "path": app_widget_group['path'].get()
                })
        self.config['apps'] = new_apps

        if storage.save_config(self.config):
            messagebox.showinfo("저장 완료", "설정이 성공적으로 저장되었습니다.")
            self.destroy()
        else:
            messagebox.showerror("저장 실패", "설정을 저장하는 데 문제가 발생했습니다.")


class App(tk.Tk):
    """메인 애플리케이션 클래스"""
    def __init__(self):
        super().__init__()
        self.title("MorningBooster")
        self.geometry("300x200")
        self.resizable(False, False)

        # 버그 수정: 'style'을 'self.style'로 변경하여 인스턴스 변수로 만듭니다.
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure("TButton", padding=10, font=('Malgun Gothic', 12, 'bold'))
        title_font = font.Font(family="Malgun Gothic", size=16, weight="bold")

        ttk.Label(self, text="MorningBooster", font=title_font).pack(pady=10)

        ttk.Button(self, text="실행", command=self._run_booster, style="Primary.TButton").pack(fill="x", padx=20, pady=5)
        ttk.Button(self, text="설정", command=self._open_settings, style="Primary.TButton").pack(fill="x", padx=20, pady=5)
        ttk.Button(self, text="도움말", command=self._show_help, style="Primary.TButton").pack(fill="x", padx=20, pady=5)

        self.style.configure("Primary.TButton", background="#4CAF50", foreground="white")
        self.style.map("Primary.TButton", background=[('active', '#4CAF50')])


    def _run_booster(self):
        config = storage.load_config()
        if not config.get("chrome_path") or not os.path.exists(config.get("chrome_path")):
            messagebox.showerror("오류", "크롬 경로가 유효하지 않습니다.\n[설정]에서 올바른 경로를 지정해주세요.")
            return

        image_name = "Gemini_Generated_Image_j4g8vij4g8vij4g8.png"
        image_path = storage.get_resource_path(os.path.join("MorningBooster", "images", image_name))
        
        LoadingScreen(self, image_path, config)


    def _open_settings(self):
        SettingsWindow(self)

    def _show_help(self):
        try:
            readme_path = storage.get_resource_path(os.path.join("MorningBooster", "README.txt"))
            with open(readme_path, 'r', encoding='utf-8') as f:
                help_text = f.read()
            
            help_win = tk.Toplevel(self)
            help_win.title("도움말")
            help_win.geometry("500x600")
            text_area = tk.Text(help_win, wrap="word", padx=10, pady=10, font=('Malgun Gothic', 10)) 
            text_area.insert(tk.END, help_text)
            text_area.config(state="disabled")
            text_area.pack(expand=True, fill="both")

        except FileNotFoundError:
            messagebox.showerror("오류", "도움말 파일을 찾을 수 없습니다.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
