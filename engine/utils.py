"""工具函数"""

import math


def normalize_angle_0_360(theta):
    """将角度归一化到 [0, 360)"""
    theta = theta % 360.0
    if theta < 0:
        theta += 360.0
    return theta


def format_value(value, precision=4):
    """格式化数值显示"""
    if value is None:
        return "—"
    if math.isnan(value) or math.isinf(value):
        return "无解"
    return f"{value:.{precision}f}".rstrip("0").rstrip(".")


def deg_to_rad(deg):
    return math.radians(deg)


def rad_to_deg(rad):
    return math.degrees(rad)


def clamp(value, lo, hi):
    """将值限制在 [lo, hi] 范围内"""
    return max(lo, min(hi, value))
