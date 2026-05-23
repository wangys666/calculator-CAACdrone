"""可复用的 UI 组件 - 精致风格"""

import tkinter as tk
from tkinter import ttk

# ---------- 全局样式常量 ----------
FONT_FAMILY = "Microsoft YaHei"
COLOR_PRIMARY = "#2c3e50"       # 深蓝灰
COLOR_ACCENT = "#3498db"        # 蓝色强调
COLOR_SUCCESS = "#27ae60"       # 绿色
COLOR_WARNING = "#e67e22"       # 橙色
COLOR_DANGER = "#e74c3c"        # 红色
COLOR_BG = "#f5f6fa"            # 浅灰背景
COLOR_CARD = "#ffffff"          # 白色卡片
COLOR_BORDER = "#dcdde1"        # 边框灰
COLOR_TEXT = "#2d3436"          # 主文字色
COLOR_TEXT_SECONDARY = "#636e72" # 次要文字
COLOR_TEXT_LIGHT = "#b2bec3"    # 浅色文字


class SectionFrame(tk.Frame):
    """带标题的卡片式分区"""

    def __init__(self, parent, title="", **kwargs):
        super().__init__(parent, bg=COLOR_CARD, **kwargs)
        self._build_ui(title)

    def _build_ui(self, title):
        if title:
            header = tk.Frame(self, bg=COLOR_CARD)
            header.pack(fill=tk.X, padx=15, pady=(12, 4))
            tk.Label(
                header,
                text=title,
                font=(FONT_FAMILY, 12, "bold"),
                fg=COLOR_PRIMARY,
                bg=COLOR_CARD,
            ).pack(anchor="w")
            tk.Frame(header, height=2, bg=COLOR_ACCENT).pack(fill=tk.X, pady=(4, 0))


class FormRow(tk.Frame):
    """一行表单：标签 + 输入框 + 单位"""

    def __init__(self, parent, label="", unit="", width=10, label_width=6, **kwargs):
        super().__init__(parent, bg=COLOR_CARD, **kwargs)
        self._unit = unit
        self._build_ui(label, unit, width, label_width)

    def _build_ui(self, label, unit, width, label_width):
        # 标签
        lbl = tk.Label(
            self,
            text=label,
            font=(FONT_FAMILY, 13),
            fg=COLOR_TEXT,
            bg=COLOR_CARD,
            width=label_width,
            anchor="e",
        )
        lbl.pack(side=tk.LEFT, padx=(0, 6))

        # 输入框
        validate_cmd = (self.register(self._validate), "%P")
        self.entry = tk.Entry(
            self,
            width=width,
            font=(FONT_FAMILY, 14),
            fg=COLOR_TEXT,
            bg="white",
            relief=tk.SOLID,
            borderwidth=1,
            justify=tk.CENTER,
            validate="key",
            validatecommand=validate_cmd,
            highlightthickness=1,
            highlightcolor=COLOR_ACCENT,
            highlightbackground=COLOR_BORDER,
        )
        self.entry.pack(side=tk.LEFT, padx=(0, 4), ipady=3)

        # 单位
        if unit:
            tk.Label(
                self,
                text=unit,
                font=(FONT_FAMILY, 11),
                fg=COLOR_TEXT_SECONDARY,
                bg=COLOR_CARD,
            ).pack(side=tk.LEFT)

    def _validate(self, value):
        if value in ("", "-", "-.", ".", "-."):
            return True
        # 允许数字、小数点、负号
        try:
            float(value)
            return True
        except ValueError:
            return False

    def get(self):
        val = self.entry.get().strip()
        if val == "":
            return None
        try:
            return float(val)
        except ValueError:
            return None

    def set(self, value):
        self.entry.delete(0, tk.END)
        if value is not None:
            # 格式化为友好显示
            if isinstance(value, float):
                text = f"{value:.4f}".rstrip("0").rstrip(".")
                self.entry.insert(0, text)
            else:
                self.entry.insert(0, str(value))

    def clear(self):
        self.entry.delete(0, tk.END)

    def config_bg(self, color):
        self.configure(bg=color)
        for child in self.winfo_children():
            if isinstance(child, (tk.Label, tk.Frame)):
                try:
                    child.configure(bg=color)
                except:
                    pass


class ActionButton(tk.Canvas):
    """圆角样式的操作按钮"""

    def __init__(self, parent, text="", command=None, bg=COLOR_ACCENT, fg="white",
                 width=120, height=38, font_size=13, **kwargs):
        super().__init__(parent, width=width, height=height,
                         bg=COLOR_BG, highlightthickness=0, **kwargs)
        self._text = text
        self._command = command
        self._bg = bg
        self._fg = fg
        self._hover_bg = self._adjust_color(bg, -20)
        self._font = (FONT_FAMILY, font_size, "bold")
        self._draw()
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def _adjust_color(self, hex_color, amount):
        r = max(0, min(255, int(hex_color[1:3], 16) + amount))
        g = max(0, min(255, int(hex_color[3:5], 16) + amount))
        b = max(0, min(255, int(hex_color[5:7], 16) + amount))
        return f"#{r:02x}{g:02x}{b:02x}"

    def _draw(self, bg=None):
        self.delete("all")
        color = bg or self._bg
        w, h = self.winfo_width() or 120, self.winfo_height() or 38
        r = 6
        self.create_rounded_rect(2, 2, w-2, h-2, r, fill=color, outline=color)
        self.create_text(w//2, h//2, text=self._text, fill=self._fg,
                         font=self._font)

    def create_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1+r, y1, x2-r, y1, x2, y1, x2, y1+r,
            x2, y2-r, x2, y2, x2-r, y2, x1+r, y2,
            x1, y2, x1, y2-r, x1, y1+r, x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _on_enter(self, e):
        self._draw(self._hover_bg)
        self.config(cursor="hand2")

    def _on_leave(self, e):
        self._draw(self._bg)
        self.config(cursor="")

    def _on_click(self, e):
        if self._command:
            self._draw(self._adjust_color(self._bg, -40))
            self.after(80, lambda: self._draw())
            self._command()


class ResultCard(tk.Frame):
    """结果展示卡片"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLOR_CARD, relief=tk.SOLID,
                         borderwidth=1, highlightbackground=COLOR_BORDER,
                         highlightcolor=COLOR_BORDER, highlightthickness=1,
                         **kwargs)
        self._build_ui()

    def _build_ui(self):
        self.text = tk.Text(
            self,
            font=("Consolas", 13),
            fg=COLOR_TEXT,
            bg=COLOR_CARD,
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=0,
            padx=12,
            pady=10,
            height=8,
        )
        self.text.pack(fill=tk.BOTH, expand=True)
        self.text.config(state=tk.DISABLED)

    def set_content(self, text):
        self.text.config(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)
        self.text.insert(1.0, text)
        self.text.config(state=tk.DISABLED)

    def clear(self):
        self.set_content("")


class SectionTitle(tk.Label):
    """分区标题"""

    def __init__(self, parent, text="", **kwargs):
        super().__init__(
            parent,
            text=text,
            font=(FONT_FAMILY, 15, "bold"),
            fg=COLOR_PRIMARY,
            bg=COLOR_BG,
            anchor="w",
            **kwargs
        )


class SmallTitle(tk.Label):
    """小标题"""

    def __init__(self, parent, text="", **kwargs):
        super().__init__(
            parent,
            text=text,
            font=(FONT_FAMILY, 12, "bold"),
            fg=COLOR_TEXT_SECONDARY,
            bg=COLOR_CARD,
            anchor="w",
            **kwargs
        )
