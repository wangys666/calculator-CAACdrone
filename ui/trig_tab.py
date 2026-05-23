"""三角函数 标签页 - 精致风格"""

import tkinter as tk
import math

from ui.widgets import (
    COLOR_BG, COLOR_CARD, COLOR_ACCENT, COLOR_WARNING,
    COLOR_TEXT, COLOR_TEXT_SECONDARY, COLOR_BORDER, COLOR_SUCCESS, COLOR_DANGER,
    FONT_FAMILY, FormRow, ResultCard, SectionTitle
)


class TrigTab(tk.Frame):
    """三角函数计算界面"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLOR_BG, **kwargs)
        self._unit = "deg"
        self._setup_ui()

    def _setup_ui(self):
        # 顶部标题区
        header = tk.Frame(self, bg=COLOR_BG, height=10)
        header.pack(fill=tk.X, padx=25, pady=(15, 5))

        SectionTitle(header, text="三角函数计算").pack(anchor="w")

        # 主内容区
        main = tk.Frame(self, bg=COLOR_BG)
        main.pack(fill=tk.BOTH, expand=True, padx=25, pady=(5, 20))

        # ---------- 输入卡片 ----------
        input_card = tk.Frame(main, bg=COLOR_CARD, relief=tk.SOLID,
                              borderwidth=1, highlightbackground=COLOR_BORDER)
        input_card.pack(fill=tk.X, pady=(0, 15), ipady=8)

        # 输入区行
        row1 = tk.Frame(input_card, bg=COLOR_CARD)
        row1.pack(fill=tk.X, padx=20, pady=(15, 8))

        tk.Label(row1, text="输入数值：", font=(FONT_FAMILY, 14),
                 fg=COLOR_TEXT, bg=COLOR_CARD).pack(side=tk.LEFT, padx=(0, 10))

        self.input_entry = tk.Entry(
            row1,
            width=14,
            font=(FONT_FAMILY, 18),
            fg=COLOR_TEXT,
            bg="white",
            relief=tk.SOLID,
            borderwidth=1,
            justify=tk.CENTER,
            highlightthickness=1,
            highlightcolor=COLOR_ACCENT,
            highlightbackground=COLOR_BORDER,
        )
        self.input_entry.pack(side=tk.LEFT, padx=(0, 20), ipady=4)
        self.input_entry.insert(0, "30")

        # 单位选择
        self.unit_var = tk.StringVar(value="deg")
        unit_frame = tk.Frame(row1, bg=COLOR_CARD)
        unit_frame.pack(side=tk.LEFT)

        for val, txt in [("deg", "度 (°)"), ("rad", "弧度 (rad)")]:
            rb = tk.Radiobutton(
                unit_frame,
                text=txt,
                variable=self.unit_var,
                value=val,
                font=(FONT_FAMILY, 12),
                fg=COLOR_TEXT,
                bg=COLOR_CARD,
                selectcolor=COLOR_CARD,
                activebackground=COLOR_CARD,
                command=self._on_unit_change,
            )
            rb.pack(side=tk.LEFT, padx=(0, 8))

        # ---------- 函数按钮网格 ----------
        btn_card = tk.Frame(main, bg=COLOR_CARD, relief=tk.SOLID,
                            borderwidth=1, highlightbackground=COLOR_BORDER)
        btn_card.pack(fill=tk.X, pady=(0, 15), ipady=10)

        btn_inner = tk.Frame(btn_card, bg=COLOR_CARD)
        btn_inner.pack(padx=20, pady=10)

        functions = [
            ("sin", self._calc_sin, "#3498db"),
            ("cos", self._calc_cos, "#3498db"),
            ("tan", self._calc_tan, "#3498db"),
            ("arcsin", self._calc_asin, COLOR_WARNING),
            ("arccos", self._calc_acos, COLOR_WARNING),
            ("arctan", self._calc_atan, COLOR_WARNING),
        ]

        self._func_btns = []
        for i, (text, cmd, color) in enumerate(functions):
            row, col = divmod(i, 3)
            btn = tk.Button(
                btn_inner,
                text=text,
                command=cmd,
                font=(FONT_FAMILY, 13, "bold"),
                bg=color,
                fg="white",
                activebackground=self._adjust_color(color, -20),
                activeforeground="white",
                relief=tk.FLAT,
                borderwidth=0,
                padx=15,
                pady=8,
                width=8,
                cursor="hand2",
            )
            btn.grid(row=row, column=col, padx=6, pady=4)
            self._func_btns.append(btn)
            # Hover effect
            btn.bind("<Enter>", lambda e, b=btn, c=color: b.config(
                bg=self._adjust_color(c, -20)))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))

        # ---------- 结果卡片 ----------
        result_card = tk.Frame(main, bg=COLOR_CARD, relief=tk.SOLID,
                               borderwidth=1, highlightbackground=COLOR_BORDER)
        result_card.pack(fill=tk.BOTH, expand=True, ipady=10)

        tk.Label(result_card, text="计算结果", font=(FONT_FAMILY, 12, "bold"),
                 fg=COLOR_TEXT_SECONDARY, bg=COLOR_CARD).pack(anchor="w", padx=20, pady=(12, 2))

        separator = tk.Frame(result_card, height=1, bg=COLOR_BORDER)
        separator.pack(fill=tk.X, padx=20, pady=(0, 8))

        self.result_var = tk.StringVar(value="点击上方按钮进行计算")
        result_label = tk.Label(
            result_card,
            textvariable=self.result_var,
            font=(FONT_FAMILY, 20, "bold"),
            fg=COLOR_ACCENT,
            bg=COLOR_CARD,
            height=2,
            anchor="center",
        )
        result_label.pack(fill=tk.X, padx=20, pady=(5, 0))

        self.formula_var = tk.StringVar(value="")
        formula_label = tk.Label(
            result_card,
            textvariable=self.formula_var,
            font=(FONT_FAMILY, 12),
            fg=COLOR_TEXT_SECONDARY,
            bg=COLOR_CARD,
        )
        formula_label.pack(padx=20, pady=(0, 12))

        # 绑定回车
        self.input_entry.bind("<Return>", lambda e: self._calc_sin())

    def _adjust_color(self, hex_color, amount):
        r = max(0, min(255, int(hex_color[1:3], 16) + amount))
        g = max(0, min(255, int(hex_color[3:5], 16) + amount))
        b = max(0, min(255, int(hex_color[5:7], 16) + amount))
        return f"#{r:02x}{g:02x}{b:02x}"

    def _get_input(self):
        try:
            val = float(self.input_entry.get().strip())
        except (ValueError, TypeError):
            self.result_var.set("请输入有效数值")
            self.formula_var.set("")
            return None, None
        if self.unit_var.get() == "deg":
            return math.radians(val), val
        return val, val

    def _format_angle(self, rad_val):
        if self.unit_var.get() == "deg":
            return f"{math.degrees(rad_val):.6f}°"
        return f"{rad_val:.6f} rad"

    def _on_unit_change(self):
        self.result_var.set("选择函数进行计算")
        self.formula_var.set("")

    def _show_result(self, text, formula=""):
        self.result_var.set(text)
        self.formula_var.set(formula)

    def _calc_sin(self):
        rad_v, orig_v = self._get_input()
        if rad_v is None:
            return
        res = math.sin(rad_v)
        u = "°" if self.unit_var.get() == "deg" else " rad"
        self._show_result(f"sin({orig_v:.4f}{u}) = {res:.6f}")

    def _calc_cos(self):
        rad_v, orig_v = self._get_input()
        if rad_v is None:
            return
        res = math.cos(rad_v)
        u = "°" if self.unit_var.get() == "deg" else " rad"
        self._show_result(f"cos({orig_v:.4f}{u}) = {res:.6f}")

    def _calc_tan(self):
        rad_v, orig_v = self._get_input()
        if rad_v is None:
            return
        if abs(math.cos(rad_v)) < 1e-12:
            self._show_result("正切值无定义（cos = 0）")
            return
        res = math.tan(rad_v)
        u = "°" if self.unit_var.get() == "deg" else " rad"
        self._show_result(f"tan({orig_v:.4f}{u}) = {res:.6f}")

    def _calc_asin(self):
        try:
            val = float(self.input_entry.get().strip())
        except (ValueError, TypeError):
            self._show_result("请输入有效数值")
            return
        if val < -1 or val > 1:
            self._show_result("输入值必须在 [-1, 1] 范围内")
            return
        res_rad = math.asin(val)
        self._show_result(f"arcsin({val}) = {self._format_angle(res_rad)}",
                          f"即 {res_rad:.6f} rad")

    def _calc_acos(self):
        try:
            val = float(self.input_entry.get().strip())
        except (ValueError, TypeError):
            self._show_result("请输入有效数值")
            return
        if val < -1 or val > 1:
            self._show_result("输入值必须在 [-1, 1] 范围内")
            return
        res_rad = math.acos(val)
        self._show_result(f"arccos({val}) = {self._format_angle(res_rad)}",
                          f"即 {res_rad:.6f} rad")

    def _calc_atan(self):
        try:
            val = float(self.input_entry.get().strip())
        except (ValueError, TypeError):
            self._show_result("请输入有效数值")
            return
        res_rad = math.atan(val)
        self._show_result(f"arctan({val}) = {self._format_angle(res_rad)}",
                          f"即 {res_rad:.6f} rad")
