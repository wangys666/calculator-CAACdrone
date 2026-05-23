"""风向航向计算引擎

根据航线角(TC)和风向(WD)确定偏流情况，计算航向角(TH)
"""

import math
from engine.utils import normalize_angle_0_360


# 8方位角映射 (显示名, 角度)
COMPASS_DIRECTIONS = [
    ("北风 N", 0),
    ("东北风 NE", 45),
    ("东风 E", 90),
    ("东南风 SE", 135),
    ("南风 S", 180),
    ("西南风 SW", 225),
    ("西风 W", 270),
    ("西北风 NW", 315),
]

# 8种偏流情况 (显示名, 相对角度, 建议修正角)
# 相对角度 = 风向(来向) - 航线角(飞机指向)
WIND_SITUATIONS = [
    ("逆风", 0, 0),          # 风迎面吹来
    ("右前侧风", 45, 10),    # 风从右前方吹来
    ("右侧风", 90, 15),      # 风从右侧吹来
    ("右后侧风", 135, 10),   # 风从右后方吹来
    ("顺风", 180, 0),        # 风从后方吹来
    ("左后侧风", -135, -10), # 风从左后方吹来
    ("左侧风", -90, -15),    # 风从左侧吹来
    ("左前侧风", -45, -10),  # 风从左前方吹来
]


def get_wind_situation(tc, wd):
    """
    根据航线角(TC)和风向(WD, 来向)判断偏流情况

    参数:
        tc: 航线角 (°)
        wd: 风向 (°, 从方向)

    返回:
        (situation_name, relative_angle, suggested_wca, angle_diff)
    """
    # 相对角度 = 风向(来向) - 航线角
    # 正: 风从航线右侧来, 负: 风从航线左侧来
    diff = (wd - tc + 360) % 360
    if diff > 180:
        diff -= 360  # 转换到 [-180, 180]

    abs_diff = abs(diff)

    # 根据相对角度匹配最近的偏流情况
    best_sit = None
    best_name = "未知"
    best_rel = 0
    best_wca = 0

    for name, rel_angle, wca in WIND_SITUATIONS:
        # 计算这个情况对应的角度范围
        if rel_angle == 180 or rel_angle == -180:
            # 顺风: 范围 157.5 ~ 180 or -180 ~ -157.5
            if abs_diff >= 157.5:
                best_sit = (name, rel_angle, wca, diff)
                break
        else:
            # 其他情况: 相对角度 ± 22.5°
            diff_from_rel = abs(diff - rel_angle)
            # 处理环绕 (例如 -45 和 315 是同一个角度)
            diff_from_rel_alt = abs(diff - (rel_angle - 360 if rel_angle > 0 else rel_angle + 360))
            min_diff = min(diff_from_rel, diff_from_rel_alt)

            if min_diff <= 22.5:
                best_sit = (name, rel_angle, wca, diff)
                break

    if best_sit is None:
        best_sit = ("未知", 0, 0, diff)

    return best_sit


def solve_heading(tc, wd, wca=None):
    """
    计算航向角

    参数:
        tc: 航线角 (°)
        wd: 风向 (°, 来向)
        wca: 偏流修正角 (°), 正=向右修正, 负=向左修正

    返回: dict
    """
    tc = normalize_angle_0_360(tc)
    wd = normalize_angle_0_360(wd)

    name, rel_angle, suggested_wca, diff = get_wind_situation(tc, wd)

    # 如果未提供 WCA，使用建议值
    if wca is None:
        wca = suggested_wca

    result = {
        "tc": tc,
        "wd": wd,
        "wca": wca,
        "situation": name,
        "rel_angle": rel_angle,
        "angle_diff": diff,
        "suggested_wca": suggested_wca,
    }

    # 计算航向角
    th = tc + wca
    result["th"] = normalize_angle_0_360(th)

    return result
