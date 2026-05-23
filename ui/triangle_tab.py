"""三角形 标签页 - 带求解和绘图功能"""

import tkinter as tk
import math

from ui.widgets import (
    COLOR_BG, COLOR_CARD, COLOR_ACCENT, COLOR_SUCCESS, COLOR_WARNING, COLOR_DANGER,
    COLOR_TEXT, COLOR_TEXT_SECONDARY, COLOR_BORDER,
    FONT_FAMILY, FormRow, SectionTitle
)
from engine.triangle_engine import solve_triangle
from engine.utils import format_value


class TriangleTab(tk.Frame):
    """三角形求解界面"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLOR_BG, **kwargs)
        self._solved_data = None
        self._setup_ui()

    def _setup_ui(self):
        header = tk.Frame(self, bg=COLOR_BG)
        header.pack(fill=tk.X, padx=25, pady=(15, 5))
        SectionTitle(header, text="三角形求解").pack(anchor="w")

        # 主内容区：左输入 + 右图形+结果
        content = tk.Frame(self, bg=COLOR_BG)
        content.pack(fill=tk.BOTH, expand=True, padx=25, pady=(5, 20))

        # ======== 左侧：输入面板 ========
        left_panel = tk.Frame(content, bg=COLOR_CARD, relief=tk.SOLID,
                              borderwidth=1, highlightbackground=COLOR_BORDER)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 12), ipady=5)

        # 说明
        tk.Label(left_panel, text="填写已知量（未知留空），点击求解",
                 font=(FONT_FAMILY, 11), fg=COLOR_TEXT_SECONDARY,
                 bg=COLOR_CARD).pack(anchor="w", padx=18, pady=(12, 8))

        # 边输入
        sides_header = tk.Frame(left_panel, bg=COLOR_CARD)
        sides_header.pack(fill=tk.X, padx=18, pady=(4, 6))
        tk.Label(sides_header, text="边长", font=(FONT_FAMILY, 12, "bold"),
                 fg="#2980b9", bg=COLOR_CARD).pack(anchor="w")

        self.a_row = FormRow(left_panel, label="边 a =", unit="", width=8, label_width=6)
        self.a_row.pack(fill=tk.X, padx=18, pady=3)
        self.b_row = FormRow(left_panel, label="边 b =", unit="", width=8, label_width=6)
        self.b_row.pack(fill=tk.X, padx=18, pady=3)
        self.c_row = FormRow(left_panel, label="边 c =", unit="", width=8, label_width=6)
        self.c_row.pack(fill=tk.X, padx=18, pady=3)

        tk.Frame(left_panel, height=1, bg=COLOR_BORDER).pack(fill=tk.X, padx=18, pady=8)

        # 角输入
        angle_header = tk.Frame(left_panel, bg=COLOR_CARD)
        angle_header.pack(fill=tk.X, padx=18, pady=(4, 6))
        tk.Label(angle_header, text="角度", font=(FONT_FAMILY, 12, "bold"),
                 fg=COLOR_WARNING, bg=COLOR_CARD).pack(anchor="w")

        self.A_row = FormRow(left_panel, label="∠A =", unit="°", width=8, label_width=6)
        self.A_row.pack(fill=tk.X, padx=18, pady=3)
        self.B_row = FormRow(left_panel, label="∠B =", unit="°", width=8, label_width=6)
        self.B_row.pack(fill=tk.X, padx=18, pady=3)
        self.C_row = FormRow(left_panel, label="∠C =", unit="°", width=8, label_width=6)
        self.C_row.pack(fill=tk.X, padx=18, pady=3)

        tk.Frame(left_panel, height=1, bg=COLOR_BORDER).pack(fill=tk.X, padx=18, pady=8)

        # 精度 + 按钮
        ctrl_frame = tk.Frame(left_panel, bg=COLOR_CARD)
        ctrl_frame.pack(fill=tk.X, padx=18, pady=(4, 12))

        tk.Label(ctrl_frame, text="精度:", font=(FONT_FAMILY, 11),
                 fg=COLOR_TEXT, bg=COLOR_CARD).pack(side=tk.LEFT, padx=(0, 5))
        self.precision_var = tk.StringVar(value="4")
        prec_combo = tk.Spinbox(
            ctrl_frame, from_=0, to=6, width=4,
            textvariable=self.precision_var,
            font=(FONT_FAMILY, 11), justify=tk.CENTER,
            relief=tk.SOLID, borderwidth=1,
            buttonbackground=COLOR_CARD,
        )
        prec_combo.pack(side=tk.LEFT, padx=(0, 15))

        solve_btn = tk.Button(
            ctrl_frame, text="求  解", font=(FONT_FAMILY, 12, "bold"),
            bg=COLOR_SUCCESS, fg="white", activebackground="#219a52",
            relief=tk.FLAT, padx=18, pady=4, cursor="hand2",
            command=self._solve,
        )
        solve_btn.pack(side=tk.LEFT, padx=(0, 8))

        clear_btn = tk.Button(
            ctrl_frame, text="清空", font=(FONT_FAMILY, 11),
            bg="#95a5a6", fg="white", activebackground="#7f8c8d",
            relief=tk.FLAT, padx=12, pady=4, cursor="hand2",
            command=self._clear_all,
        )
        clear_btn.pack(side=tk.LEFT)

        # ======== 右侧：图形 + 结果 ========
        right_panel = tk.Frame(content, bg=COLOR_CARD, relief=tk.SOLID,
                               borderwidth=1, highlightbackground=COLOR_BORDER)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 标题
        tk.Label(right_panel, text="三角形示意图", font=(FONT_FAMILY, 12, "bold"),
                 fg=COLOR_TEXT_SECONDARY, bg=COLOR_CARD).pack(anchor="w", padx=18, pady=(12, 2))

        # Canvas
        self.canvas = tk.Canvas(
            right_panel, bg="white", highlightthickness=1,
            highlightbackground=COLOR_BORDER, height=220,
        )
        self.canvas.pack(fill=tk.X, padx=15, pady=(5, 10))
        self._draw_default_triangle()

        # 结果区域
        self.result_frame = tk.LabelFrame(
            right_panel, text=" 计算结果 ",
            font=(FONT_FAMILY, 11, "bold"), fg=COLOR_ACCENT,
            bg=COLOR_CARD, padx=10, pady=8,
            relief=tk.SOLID, borderwidth=1,
            highlightbackground=COLOR_BORDER,
        )
        self.result_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        self.result_text = tk.Text(
            self.result_frame,
            font=("Consolas", 11),
            fg=COLOR_TEXT, bg="white",
            wrap=tk.WORD, relief=tk.FLAT,
            borderwidth=0, padx=10, pady=8,
            height=7,
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        self.result_text.config(state=tk.DISABLED)

    def _get_precision(self):
        try:
            return int(self.precision_var.get())
        except (ValueError, TypeError):
            return 4

    def _solve(self):
        a = self.a_row.get()
        b = self.b_row.get()
        c = self.c_row.get()
        A = self.A_row.get()
        B = self.B_row.get()
        C = self.C_row.get()

        known_count = sum(1 for v in [a, b, c, A, B, C] if v is not None)

        if known_count < 3:
            self._show_result("至少需要输入 3 个已知量")
            self._draw_default_triangle()
            return

        prec = self._get_precision()
        result = solve_triangle(a, b, c, A, B, C, precision=prec)

        if "error" in result:
            self._show_result(f"错误: {result['error']}")
            self._draw_default_triangle()
            self._solved_data = None
            return

        self._solved_data = result
        self._display_result(result)
        self._draw_solved_triangle(result)

    def _display_result(self, r):
        prec = self._get_precision()
        lines = []
        lines.append(f"  a = {format_value(r.get('a'), prec)}")
        lines.append(f"  b = {format_value(r.get('b'), prec)}")
        lines.append(f"  c = {format_value(r.get('c'), prec)}")
        lines.append(f"  A = {format_value(r.get('A'), prec)}°")
        lines.append(f"  B = {format_value(r.get('B'), prec)}°")
        lines.append(f"  C = {format_value(r.get('C'), prec)}°")
        lines.append(f"  面积 = {format_value(r.get('area'), prec)}")

        # 校验内角和
        if r.get("A") is not None and r.get("B") is not None and r.get("C") is not None:
            s = r["A"] + r["B"] + r["C"]
            lines.append(f"  内角和 = {s:.2f}°")

        self._show_result("\n".join(lines))

    def _show_result(self, text):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, text)
        self.result_text.config(state=tk.DISABLED)

    def _clear_all(self):
        for row in [self.a_row, self.b_row, self.c_row, self.A_row, self.B_row, self.C_row]:
            row.clear()
        self._show_result("")
        self._draw_default_triangle()
        self._solved_data = None

    def _draw_default_triangle(self):
        """绘制默认的占位三角形"""
        self.canvas.delete("all")
        w = self.canvas.winfo_width() or 380
        h = self.canvas.winfo_height() or 220
        cx, cy = w // 2, h // 2 + 5
        s = min(w, h) * 0.35

        Ax, Ay = cx, cy - s
        Bx, By = cx - s * 0.866, cy + s * 0.5
        Cx, Cy = cx + s * 0.866, cy + s * 0.5

        self._draw_triangle_on_canvas(Ax, Ay, Bx, By, Cx, Cy, temp=True)

    def _draw_solved_triangle(self, r):
        """根据求解结果绘制三角形"""
        self.canvas.delete("all")
        w = self.canvas.winfo_width() or 380
        h = self.canvas.winfo_height() or 220

        a = r.get("a", 1)
        b = r.get("b", 1)
        c = r.get("c", 1)

        if not all([a, b, c]):
            self._draw_default_triangle()
            return

        if a <= 0 or b <= 0 or c <= 0:
            self._draw_default_triangle()
            return

        # 按比例缩放绘制
        # 将三角形放在 Canvas 中心
        # 先计算三角形顶点坐标（标准位置：C 在 (0,0), B 在 (a,0)）
        # A 的位置由 b 和 c（以及角 C）确定
        C_rad = math.acos((a**2 + b**2 - c**2) / (2 * a * b))

        # 坐标: C 在原点, B 在 x 轴正方向 a 处
        # A 在: (b * cos(C), b * sin(C))
        pC = (0.0, 0.0)
        pB = (a, 0.0)
        pA = (b * math.cos(C_rad), b * math.sin(C_rad))

        # 计算缩放和平移
        xs = [pA[0], pB[0], pC[0]]
        ys = [pA[1], pB[1], pC[1]]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        tri_w = max_x - min_x
        tri_h = max_y - min_y

        if tri_w < 1e-10 or tri_h < 1e-10:
            self._draw_default_triangle()
            return

        margin = 75
        avail_w = w - 2 * margin
        avail_h = h - 2 * margin
        scale = min(avail_w / tri_w, avail_h / tri_h)

        # 平移到 Canvas 中心
        center_x = w / 2
        center_y = h / 2
        mid_x = (min_x + max_x) / 2
        mid_y = (min_y + max_y) / 2

        def transform(x, y):
            dx = (x - mid_x) * scale
            dy = (y - mid_y) * scale
            return center_x + dx, center_y - dy  # y 翻转

        Ax, Ay = transform(*pA)
        Bx, By = transform(*pB)
        Cx, Cy = transform(*pC)

        self._draw_triangle_on_canvas(Ax, Ay, Bx, By, Cx, Cy, temp=False, r=r)

    def _draw_triangle_on_canvas(self, Ax, Ay, Bx, By, Cx, Cy, temp=True, r=None):
        """在 Canvas 上绘制三角形"""
        self.canvas.delete("all")
        w = self.canvas.winfo_width() or 380

        # 画边
        self.canvas.create_line(Ax, Ay, Bx, By, width=2.5, fill="#2980b9")
        self.canvas.create_line(Bx, By, Cx, Cy, width=2.5, fill="#2980b9")
        self.canvas.create_line(Cx, Cy, Ax, Ay, width=2.5, fill="#2980b9")

        # 计算边的中点
        AB_mid = ((Ax + Bx) / 2, (Ay + By) / 2)
        BC_mid = ((Bx + Cx) / 2, (By + Cy) / 2)
        CA_mid = ((Cx + Ax) / 2, (Cy + Ay) / 2)

        # 边中点偏移方向（向外）
        cx, cy = (Ax + Bx + Cx) / 3, (Ay + By + Cy) / 3

        def offset_outside(px, py, dist=18):
            """沿 (重心→点) 方向外推 dist 像素"""
            dx = px - cx
            dy = py - cy
            d = math.sqrt(dx*dx + dy*dy)
            if d < 1:
                return px, py - dist
            return px + dx/d * dist, py + dy/d * dist

        AB_out = offset_outside(*AB_mid)
        BC_out = offset_outside(*BC_mid)
        CA_out = offset_outside(*CA_mid)

        # 顶点标签外推距离更大，避免压在边线上
        A_out = offset_outside(Ax, Ay, dist=28)
        B_out = offset_outside(Bx, By, dist=28)
        C_out = offset_outside(Cx, Cy, dist=28)

        if temp:
            # 占位模式 - 显示通用标签
            self.canvas.create_text(AB_out, text="c", font=("Microsoft YaHei", 12, "italic"),
                                    fill="#2980b9")
            self.canvas.create_text(BC_out, text="a", font=("Microsoft YaHei", 12, "italic"),
                                    fill="#2980b9")
            self.canvas.create_text(CA_out, text="b", font=("Microsoft YaHei", 12, "italic"),
                                    fill="#2980b9")
            self.canvas.create_text(A_out, text="A", font=("Microsoft YaHei", 13, "bold"),
                                    fill="#e67e22")
            self.canvas.create_text(B_out, text="B", font=("Microsoft YaHei", 13, "bold"),
                                    fill="#e67e22")
            self.canvas.create_text(C_out, text="C", font=("Microsoft YaHei", 13, "bold"),
                                    fill="#e67e22")
            self.canvas.create_text(w//2, 18, text="输入已知量后点击求解",
                                    font=("Microsoft YaHei", 10), fill="#b2bec3")
        elif r is not None:
            prec = self._get_precision()
            # 显示实际值
            self.canvas.create_text(AB_out, text=f"c={format_value(r.get('c'), prec)}",
                                    font=("Microsoft YaHei", 10), fill="#2980b9")
            self.canvas.create_text(BC_out, text=f"a={format_value(r.get('a'), prec)}",
                                    font=("Microsoft YaHei", 10), fill="#2980b9")
            self.canvas.create_text(CA_out, text=f"b={format_value(r.get('b'), prec)}",
                                    font=("Microsoft YaHei", 10), fill="#2980b9")

            # 顶点标签 - 沿重心向外的方向放置
            self.canvas.create_text(A_out, text=f"A\n{format_value(r.get('A'), prec)}°",
                                    font=("Microsoft YaHei", 10), fill="#e67e22",
                                    justify=tk.CENTER)
            self.canvas.create_text(B_out, text=f"B\n{format_value(r.get('B'), prec)}°",
                                    font=("Microsoft YaHei", 10), fill="#e67e22",
                                    justify=tk.CENTER)
            self.canvas.create_text(C_out, text=f"C\n{format_value(r.get('C'), prec)}°",
                                    font=("Microsoft YaHei", 10), fill="#e67e22",
                                    justify=tk.CENTER)
