"""风向航向 标签页"""

import tkinter as tk

from ui.widgets import (
    COLOR_BG, COLOR_CARD, COLOR_PRIMARY, COLOR_ACCENT, COLOR_TEXT,
    COLOR_TEXT_SECONDARY, COLOR_BORDER, FONT_FAMILY
)


def _norm_angle(a):
    """归一化到 [0, 360)"""
    return a % 360


class WindTab(tk.Frame):
    """风向航向计算界面"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLOR_BG, **kwargs)
        self._selected_situation = "逆风"
        self._selected_rel_angle = 0
        self._setup_ui()

    def _setup_ui(self):
        card = tk.Frame(self, bg=COLOR_CARD, relief=tk.SOLID,
                        borderwidth=1, highlightbackground=COLOR_BORDER)
        card.pack(fill=tk.BOTH, expand=True)

        # ---- 上方输入区（横向两列） ----
        top = tk.Frame(card, bg=COLOR_CARD)
        top.pack(fill=tk.X, padx=25, pady=(18, 8))

        # ===== 左列：第1步 风向 =====
        left_col = tk.Frame(top, bg=COLOR_CARD)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))

        self._add_section_title(left_col, "第1步：输入风向角度")

        wd_frame = tk.Frame(left_col, bg=COLOR_CARD)
        wd_frame.pack(fill=tk.X, pady=(10, 6))
        tk.Label(wd_frame, text="风向角度:", font=(FONT_FAMILY, 16),
                 fg=COLOR_PRIMARY, bg=COLOR_CARD).pack(side=tk.LEFT, padx=(0, 12))
        self.wd_entry = self._make_entry(wd_frame, 270, width=6)
        tk.Label(wd_frame, text="°", font=(FONT_FAMILY, 16),
                 fg=COLOR_TEXT_SECONDARY, bg=COLOR_CARD).pack(side=tk.LEFT, padx=(6, 0))

        compass_frame = tk.Frame(left_col, bg=COLOR_CARD)
        compass_frame.pack(fill=tk.X, pady=(4, 4))

        btn_data = [
            ("北 N\n0°", 0), ("东北 NE\n45°", 45),
            ("东 E\n90°", 90), ("东南 SE\n135°", 135),
            ("南 S\n180°", 180), ("西南 SW\n225°", 225),
            ("西 W\n270°", 270), ("西北 NW\n315°", 315),
        ]
        for i, (text, a) in enumerate(btn_data):
            r, c = divmod(i, 4)
            tk.Button(compass_frame, text=text, font=(FONT_FAMILY, 10),
                      bg="white", fg=COLOR_PRIMARY,
                      activebackground=COLOR_PRIMARY, activeforeground="white",
                      relief=tk.SOLID, borderwidth=1, width=9, height=2,
                      cursor="hand2",
                      command=lambda a=a: self._set_wd(a)
                      ).grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
            compass_frame.grid_columnconfigure(c, weight=1)
        compass_frame.grid_rowconfigure(0, weight=1)
        compass_frame.grid_rowconfigure(1, weight=1)

        # ===== 右列：第2步 偏流修正角 =====
        right_col = tk.Frame(top, bg=COLOR_CARD)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(15, 0))

        self._add_section_title(right_col, "第2步：偏流修正角")

        sit_frame = tk.Frame(right_col, bg=COLOR_CARD)
        sit_frame.pack(fill=tk.X, pady=(10, 6))

        tk.Label(sit_frame, text="选择风对飞机的影响:", font=(FONT_FAMILY, 11),
                 fg=COLOR_TEXT_SECONDARY, bg=COLOR_CARD).pack(anchor="w", pady=(0, 4))

        btn_grid = tk.Frame(sit_frame, bg=COLOR_CARD)
        btn_grid.pack(fill=tk.X)

        layout = [
            ("逆风\n0°", 0, "逆风"),
            ("右前侧风\n+45°", 45, "右前侧风"),
            ("右侧风\n+90°", 90, "右侧风"),
            ("右后侧风\n+135°", 135, "右后侧风"),
            ("顺风\n180°", 180, "顺风"),
            ("左后侧风\n-135°", -135, "左后侧风"),
            ("左侧风\n-90°", -90, "左侧风"),
            ("左前侧风\n-45°", -45, "左前侧风"),
        ]
        for i, (text, angle, sit) in enumerate(layout):
            r, c = divmod(i, 4)
            tk.Button(btn_grid, text=text, font=(FONT_FAMILY, 10),
                      bg="white", fg=COLOR_PRIMARY,
                      activebackground=COLOR_PRIMARY, activeforeground="white",
                      relief=tk.SOLID, borderwidth=1, width=9, height=2,
                      cursor="hand2",
                      command=lambda a=angle, s=sit: self._set_wind_effect(a, s)
                      ).grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
            btn_grid.grid_columnconfigure(c, weight=1)
        btn_grid.grid_rowconfigure(0, weight=1)
        btn_grid.grid_rowconfigure(1, weight=1)

        wca_frame = tk.Frame(right_col, bg=COLOR_CARD)
        wca_frame.pack(fill=tk.X, pady=(10, 4))
        tk.Label(wca_frame, text="偏流修正角:", font=(FONT_FAMILY, 14),
                 fg=COLOR_PRIMARY, bg=COLOR_CARD).pack(side=tk.LEFT, padx=(0, 8))
        self.wca_entry = self._make_entry(wca_frame, 0, width=6)
        # tk.Label(wca_frame, text="°（正=向右）", font=(FONT_FAMILY, 11),
        #          fg=COLOR_TEXT_SECONDARY, bg=COLOR_CARD).pack(side=tk.LEFT, padx=(6, 0))

        # ---- 分隔线 ----
        tk.Frame(card, height=1, bg=COLOR_BORDER).pack(fill=tk.X, padx=25, pady=6)

        # ---- 计算按钮 + 结果 ----
        bottom = tk.Frame(card, bg=COLOR_CARD)
        bottom.pack(fill=tk.BOTH, expand=True, padx=25, pady=(6, 20))

        # 计算按钮
        btn_frame = tk.Frame(bottom, bg=COLOR_CARD)
        btn_frame.pack(fill=tk.X, pady=(4, 12))
        tk.Button(btn_frame, text="计算航向角", font=(FONT_FAMILY, 16, "bold"),
                  bg=COLOR_PRIMARY, fg="white", activebackground="#34495e",
                  relief=tk.FLAT, borderwidth=0, padx=35, pady=10, cursor="hand2",
                  command=self._calculate
                  ).pack(anchor="center")

        # 结果区域
        result_frame = tk.Frame(bottom, bg=COLOR_CARD)
        result_frame.pack(fill=tk.BOTH, expand=True)

        tk.Frame(result_frame, height=2, bg=COLOR_PRIMARY).pack(fill=tk.X)

        self.result_var = tk.StringVar(value="航向角：— °")
        tk.Label(result_frame, textvariable=self.result_var,
                 font=(FONT_FAMILY, 38, "bold"), fg=COLOR_ACCENT,
                 bg=COLOR_CARD, anchor="center"
                 ).pack(fill=tk.X, pady=(25, 8))

        self.detail_var = tk.StringVar(value="")
        tk.Label(result_frame, textvariable=self.detail_var,
                 font=(FONT_FAMILY, 14), fg=COLOR_TEXT,
                 bg=COLOR_CARD, justify=tk.CENTER
                 ).pack(fill=tk.X, padx=20, pady=(4, 0))

    # ====== 工具 ======

    def _add_section_title(self, parent, text):
        h = tk.Frame(parent, bg=COLOR_CARD)
        h.pack(fill=tk.X, pady=(8, 4))
        tk.Label(h, text=text, font=(FONT_FAMILY, 13, "bold"),
                 fg=COLOR_PRIMARY, bg=COLOR_CARD).pack(anchor="w")
        tk.Frame(h, height=2, bg=COLOR_PRIMARY).pack(fill=tk.X, pady=(4, 0))

    def _make_entry(self, parent, default_val=0, width=10):
        vcmd = (self.register(self._valid), "%P")
        e = tk.Entry(parent, width=width, font=(FONT_FAMILY, 18),
                     fg=COLOR_PRIMARY, bg="white", relief=tk.SOLID,
                     borderwidth=1, justify=tk.CENTER, validate="key",
                     validatecommand=vcmd, highlightthickness=1,
                     highlightcolor=COLOR_PRIMARY, highlightbackground=COLOR_BORDER)
        e.pack(side=tk.LEFT, ipady=6)
        e.insert(0, str(default_val))
        return e

    def _valid(self, v):
        if v in ("", "-", "-.", ".", "-."):
            return True
        try:
            float(v)
            return True
        except ValueError:
            return False

    def _get_val(self, entry):
        try:
            return float(entry.get().strip())
        except (ValueError, TypeError):
            return None

    def _set_wd(self, angle):
        self.wd_entry.delete(0, tk.END)
        self.wd_entry.insert(0, str(angle))

    def _set_wind_effect(self, angle, sit_name):
        self._selected_situation = sit_name
        self._selected_rel_angle = angle
        self.wca_entry.delete(0, tk.END)
        self.wca_entry.insert(0, str(angle))

    # ====== 计算 ======

    def _calculate(self):
        wd = self._get_val(self.wd_entry)
        wca = self._get_val(self.wca_entry)
        if wd is None:
            self.result_var.set("航向角：— °")
            self.detail_var.set("请输入风向角度")
            return
        if wca is None:
            wca = 0

        th = _norm_angle(wd - wca)

        self.result_var.set(f"航向角：{th:.1f}°")

        sig = "+" if wca >= 0 else ""
        self.detail_var.set(
            f"风向 {wd:.0f}°    偏流修正角 {sig}{wca:.0f}°\n"
            f"偏流情况：{self._selected_situation}"
        )
