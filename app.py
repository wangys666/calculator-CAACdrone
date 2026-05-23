"""主窗口 - 科学计算器"""

import tkinter as tk
from tkinter import ttk

from ui.trig_tab import TrigTab
from ui.triangle_tab import TriangleTab
from ui.wind_tab import WindTab
from ui.widgets import COLOR_BG, COLOR_PRIMARY, FONT_FAMILY


class App(tk.Tk):
    """科学计算器 主窗口"""

    def __init__(self):
        super().__init__()

        self.title("科学计算器")
        self.geometry("950x680")
        self.minsize(800, 600)

        # 居中窗口
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

        # 设置样式
        self._setup_style()

        # 应用标题栏
        title_bar = tk.Frame(self, bg=COLOR_PRIMARY, height=48)
        title_bar.pack(fill=tk.X, side=tk.TOP)
        title_bar.pack_propagate(False)

        tk.Label(
            title_bar,
            text="科学计算器",
            font=(FONT_FAMILY, 18, "bold"),
            fg="white",
            bg=COLOR_PRIMARY,
        ).pack(side=tk.LEFT, padx=20, pady=8)

        # 创建标签页
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        self.trig_tab = TrigTab(self.notebook)
        self.triangle_tab = TriangleTab(self.notebook)
        self.wind_tab = WindTab(self.notebook)

        self.notebook.add(self.trig_tab, text="  三角函数  ")
        self.notebook.add(self.triangle_tab, text="  三角形  ")
        self.notebook.add(self.wind_tab, text="  风向航向  ")

        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = tk.Label(
            self,
            textvariable=self.status_var,
            font=(FONT_FAMILY, 9),
            fg=COLOR_PRIMARY,
            bd=0,
            relief=tk.FLAT,
            anchor="w",
            padx=15,
            pady=3,
            bg="#ecf0f1",
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def _setup_style(self):
        style = ttk.Style()
        for theme in ("vista", "aqua", "clam", "default"):
            if theme in style.theme_names():
                style.theme_use(theme)
                break
        style.configure(
            "TNotebook",
            background=COLOR_BG,
            borderwidth=0,
            tabmargins=[0, 0, 0, 0],
        )
        style.configure(
            "TNotebook.Tab",
            font=(FONT_FAMILY, 12),
            padding=[20, 8],
            borderwidth=0,
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", "white"), ("active", "#ecf0f1")],
            foreground=[("selected", COLOR_PRIMARY)],
        )
