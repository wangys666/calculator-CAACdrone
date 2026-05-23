"""三角形求解引擎

支持: SSS, SAS, ASA, AAS, SSA
使用正弦定理和余弦定理
"""

import math
from engine.utils import rad_to_deg, deg_to_rad, format_value


class TriangleSolver:
    """三角形求解器"""

    def __init__(self, precision=4):
        self.precision = precision

    def solve(self, a=None, b=None, c=None, A=None, B=None, C=None):
        """
        求解三角形
        输入: 任意边(a,b,c)和角(A,B,C) - 未知传 None
        返回: dict 包含所有 6 个量 + area, 或 dict 包含 error 信息
        """
        # 角度转弧度
        A_r = deg_to_rad(A) if A is not None else None
        B_r = deg_to_rad(B) if B is not None else None
        C_r = deg_to_rad(C) if C is not None else None

        known_count = sum(1 for v in [a, b, c, A_r, B_r, C_r] if v is not None)

        if known_count < 3:
            return {"error": "至少需要输入 3 个已知量"}

        # 检查是否只有角没有边
        sides_known = sum(1 for v in [a, b, c] if v is not None)
        if sides_known == 0:
            return {"error": "至少需要输入 1 条边长"}

        try:
            result = self._solve_internal(a, b, c, A_r, B_r, C_r)
            if result:
                # 弧度转角度
                for key in ["A", "B", "C"]:
                    if result.get(key) is not None:
                        result[key] = rad_to_deg(result[key])
                # 计算面积
                if all(result.get(k) is not None for k in ["a", "b", "C"]):
                    result["area"] = 0.5 * result["a"] * result["b"] * math.sin(deg_to_rad(result["C"]))
                elif all(result.get(k) is not None for k in ["a", "c", "B"]):
                    result["area"] = 0.5 * result["a"] * result["c"] * math.sin(deg_to_rad(result["B"]))
                elif all(result.get(k) is not None for k in ["b", "c", "A"]):
                    result["area"] = 0.5 * result["b"] * result["c"] * math.sin(deg_to_rad(result["A"]))
                return result
            return {"error": "无法求解，请检查输入值"}
        except (ValueError, ZeroDivisionError) as e:
            return {"error": str(e)}

    def _solve_internal(self, a, b, c, A, B, C):
        """内部求解，所有角度使用弧度"""
        # 检查确保三条边满足三角不等式
        sides = [a, b, c]
        known_sides = [s for s in sides if s is not None]
        if len(known_sides) >= 3:
            s1, s2, s3 = sorted(known_sides[:3])
            if s1 + s2 <= s3:
                raise ValueError("两边之和必须大于第三边")

        # 尝试不同方法
        # 先用余弦定理解 SSS, SAS
        methods = [
            (self._try_sss, [a, b, c, A, B, C]),
            (self._try_sas, [a, b, c, A, B, C]),
            (self._try_asa_aas, [a, b, c, A, B, C]),
            (self._try_ssa, [a, b, c, A, B, C]),
        ]

        for method, args in methods:
            result = method(*args)
            if result and self._is_complete(result):
                return result

        return None

    def _is_complete(self, r):
        """检查是否所有 6 个量都已知"""
        return all(r.get(k) is not None for k in ["a", "b", "c", "A", "B", "C"])

    def _has_progress(self, r):
        """检查是否有求解进展"""
        known = sum(1 for k in ["a", "b", "c", "A", "B", "C"] if r.get(k) is not None)
        return known > 3

    def _try_sss(self, a, b, c, A, B, C):
        """三边已知"""
        # todo 这里就没有更优雅的写法吗
        if a is None or b is None or c is None:
            return None

        # 余弦定理求角
        A_val = math.acos((b**2 + c**2 - a**2) / (2 * b * c))
        B_val = math.acos((a**2 + c**2 - b**2) / (2 * a * c))
        C_val = math.acos((a**2 + b**2 - c**2) / (2 * a * b))
        return {"a": a, "b": b, "c": c, "A": A_val, "B": B_val, "C": C_val}

    def _try_sas(self, a, b, c, A, B, C):
        """两边及其夹角已知"""
        # 两边 a, b 夹角 C
        if a is not None and b is not None and C is not None and c is None:
            c_val = math.sqrt(a**2 + b**2 - 2 * a * b * math.cos(C))
            A_val = math.acos((b**2 + c_val**2 - a**2) / (2 * b * c_val))
            B_val = math.acos((a**2 + c_val**2 - b**2) / (2 * a * c_val))
            return {"a": a, "b": b, "c": c_val, "A": A_val, "B": B_val, "C": C}

        # 两边 b, c 夹角 A
        if b is not None and c is not None and A is not None and a is None:
            a_val = math.sqrt(b**2 + c**2 - 2 * b * c * math.cos(A))
            B_val = math.acos((a_val**2 + c**2 - b**2) / (2 * a_val * c))
            C_val = math.acos((a_val**2 + b**2 - c**2) / (2 * a_val * b))
            return {"a": a_val, "b": b, "c": c, "A": A, "B": B_val, "C": C_val}

        # 两边 a, c 夹角 B
        if a is not None and c is not None and B is not None and b is None:
            b_val = math.sqrt(a**2 + c**2 - 2 * a * c * math.cos(B))
            A_val = math.acos((b_val**2 + c**2 - a**2) / (2 * b_val * c))
            C_val = math.acos((a**2 + b_val**2 - c**2) / (2 * a * b_val))
            return {"a": a, "b": b_val, "c": c, "A": A_val, "B": B, "C": C_val}

        return None

    def _try_asa_aas(self, a, b, c, A, B, C):
        """两角及其夹边 / 两角及一对边"""
        angles = [A, B, C]
        known_angles = [(i, v) for i, v in enumerate(("A", "B", "C")) if angles[["A", "B", "C"].index(v)] if False]
        # 重构
        known_angles = []
        for name in ["A", "B", "C"]:
            val = locals()[name]
            if val is not None:
                known_angles.append((name, val))

        if len(known_angles) < 2:
            return None

        # 确定已知角
        if A is not None and B is not None and C is None:
            C = math.pi - A - B
        elif A is not None and C is not None and B is None:
            B = math.pi - A - C
        elif B is not None and C is not None and A is None:
            A = math.pi - B - C
        else:
            # 所有角已知，检查是否合理
            if A is not None and B is not None and C is not None:
                if abs(A + B + C - math.pi) > 1e-10:
                    raise ValueError("三角形内角和必须等于 180°")
            else:
                return None

        # 检查是否有效
        if A <= 0 or B <= 0 or C <= 0:
            raise ValueError("角度必须大于 0°")

        # 如果有一条边已知，用正弦定理求其他边
        sides = {"a": a, "b": b, "c": c}
        known_side = None
        for name, val in sides.items():
            if val is not None:
                known_side = (name, val)
                break

        if known_side is None:
            return None

        name, val = known_side

        # a/sin(A) = b/sin(B) = c/sin(C) = 2R
        if name == "a":
            side_ratio = a / math.sin(A)
            a_val = a
            b_val = side_ratio * math.sin(B)
            c_val = side_ratio * math.sin(C)
        elif name == "b":
            side_ratio = b / math.sin(B)
            a_val = side_ratio * math.sin(A)
            b_val = b
            c_val = side_ratio * math.sin(C)
        else:  # 'c'
            side_ratio = c / math.sin(C)
            a_val = side_ratio * math.sin(A)
            b_val = side_ratio * math.sin(B)
            c_val = c

        return {"a": a_val, "b": b_val, "c": c_val, "A": A, "B": B, "C": C}

    def _try_ssa(self, a, b, c, A, B, C):
        """SSA: 已知两边与其中一边的对角(可能歧义)。

        通过 (边名, 对角名) 配对识别所有 6 种 SSA 组态:
          (a,b,A) (a,b,B) (a,c,A) (a,c,C) (b,c,B) (b,c,C)
        其中"已知角"必须是某条"已知边"的对角(否则就是 SAS,
        应已被 _try_sas 处理)。
        """
        sides = {"a": a, "b": b, "c": c}
        angles = {"A": A, "B": B, "C": C}
        known_sides = [n for n, v in sides.items() if v is not None]
        known_angles = [n for n, v in angles.items() if v is not None]
        if len(known_sides) != 2 or len(known_angles) != 1:
            return None

        ang_name = known_angles[0]
        opp_name = ang_name.lower()              # 已知角的对边
        if opp_name not in known_sides:
            return None                          # 已知角夹在两边之间 → SAS
        adj_name = next(n for n in known_sides if n != opp_name)
        third_name = next(n for n in "abc" if n not in known_sides)

        side_opp = sides[opp_name]
        side_adj = sides[adj_name]
        angle_opp = angles[ang_name]

        # 正弦定理: sin(adj_angle)/side_adj = sin(angle_opp)/side_opp
        sin_adj = side_adj * math.sin(angle_opp) / side_opp
        if sin_adj > 1 + 1e-9:
            raise ValueError("无解：已知角的对边过短")
        sin_adj = max(-1.0, min(1.0, sin_adj))
        asin_val = math.asin(sin_adj)

        # 两个候选 adj_angle (锐 + 钝); 当 sin_adj == 1 时两者重合
        adj_candidates = [asin_val]
        if asin_val < math.pi / 2 - 1e-9:
            adj_candidates.append(math.pi - asin_val)

        solutions = []
        for adj_val in adj_candidates:
            third_val = math.pi - angle_opp - adj_val
            if adj_val > 1e-9 and third_val > 1e-9:
                side_third = side_opp * math.sin(third_val) / math.sin(angle_opp)
                solutions.append({
                    opp_name: side_opp,
                    adj_name: side_adj,
                    third_name: side_third,
                    ang_name: angle_opp,
                    adj_name.upper(): adj_val,
                    third_name.upper(): third_val,
                })

        if not solutions:
            raise ValueError("无解：角度组合无效")

        # 主解(锐角分支); 若存在钝角分支保留歧义提示
        primary = solutions[0]
        if len(solutions) > 1:
            primary["ambiguous"] = True
        return primary


def solve_triangle(a=None, b=None, c=None, A=None, B=None, C=None, precision=4):
    """便捷调用"""
    solver = TriangleSolver(precision)
    result = solver.solve(a, b, c, A, B, C)
    return result
