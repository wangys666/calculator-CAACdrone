"""SSA (两边一对角) 求解测试

覆盖 6 个配置 + 歧义解 + 无解 + 边界情形。
"""

import math
import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.triangle_engine import solve_triangle


def approx(x, y, tol=1e-3):
    return abs(x - y) < tol


class TestSSA(unittest.TestCase):

    def _check(self, r, **expected):
        self.assertNotIn("error", r, msg=f"unexpected error: {r.get('error')}")
        for k, v in expected.items():
            self.assertIsNotNone(r.get(k), msg=f"{k} missing in {r}")
            self.assertTrue(
                approx(r[k], v),
                msg=f"{k}: got {r[k]}, expected {v}",
            )
        s = r["A"] + r["B"] + r["C"]
        self.assertTrue(approx(s, 180.0), msg=f"angles sum to {s}, expected 180")

    # ---- 6 configurations: each (two sides, one of the angles opposite a known side) ----

    def test_ab_A(self):
        # a=7, b=10, A=30°  classic ambiguous; principal (acute B) solution
        r = solve_triangle(a=7, b=10, A=30)
        self._check(r, a=7, b=10, A=30)
        self.assertTrue(approx(r["B"], 45.5847, tol=1e-3))
        self.assertTrue(approx(r["C"], 104.4153, tol=1e-3))

    def test_ab_B(self):
        # mirror: a=10, b=7, B=30°  (was missing!)
        r = solve_triangle(a=10, b=7, B=30)
        self._check(r, a=10, b=7, B=30)
        self.assertTrue(approx(r["A"], 45.5847, tol=1e-3))
        self.assertTrue(approx(r["C"], 104.4153, tol=1e-3))

    def test_ac_A(self):
        r = solve_triangle(a=7, c=10, A=30)
        self._check(r, a=7, c=10, A=30)
        self.assertTrue(approx(r["C"], 45.5847, tol=1e-3))
        self.assertTrue(approx(r["B"], 104.4153, tol=1e-3))

    def test_ac_C(self):
        # was missing!
        r = solve_triangle(a=10, c=7, C=30)
        self._check(r, a=10, c=7, C=30)
        self.assertTrue(approx(r["A"], 45.5847, tol=1e-3))
        self.assertTrue(approx(r["B"], 104.4153, tol=1e-3))

    def test_bc_B(self):
        r = solve_triangle(b=7, c=10, B=30)
        self._check(r, b=7, c=10, B=30)
        self.assertTrue(approx(r["C"], 45.5847, tol=1e-3))
        self.assertTrue(approx(r["A"], 104.4153, tol=1e-3))

    def test_bc_C(self):
        # was missing!
        r = solve_triangle(b=10, c=7, C=30)
        self._check(r, b=10, c=7, C=30)
        self.assertTrue(approx(r["B"], 45.5847, tol=1e-3))
        self.assertTrue(approx(r["A"], 104.4153, tol=1e-3))

    # ---- single-solution branches ----

    def test_single_solution_opposite_obtuse(self):
        # angle_opp obtuse, side_opp > side_adj → unique solution
        r = solve_triangle(a=10, b=5, A=120)
        self._check(r, a=10, b=5, A=120)
        # sin(B) = 5 * sin(120) / 10 = √3/4 ≈ 0.4330  → B = 25.6589°
        self.assertTrue(approx(r["B"], 25.6589, tol=1e-3))
        self.assertTrue(approx(r["C"], 34.3411, tol=1e-3))

    def test_single_solution_side_opp_ge_side_adj(self):
        # angle_opp acute and side_opp >= side_adj → unique (B acute)
        r = solve_triangle(a=10, b=5, A=30)
        self._check(r, a=10, b=5, A=30)
        # sin(B) = 5 * 0.5 / 10 = 0.25 → B = 14.4775°
        self.assertTrue(approx(r["B"], 14.4775, tol=1e-3))

    # ---- no solution / degenerate ----

    def test_no_solution_too_short(self):
        # a < b*sin(A)  → no triangle
        r = solve_triangle(a=4, b=10, A=30)  # h = 5, a=4 < 5
        self.assertIn("error", r)

    def test_no_solution_obtuse_opp_small(self):
        # angle_opp obtuse but side_opp ≤ side_adj → no solution
        r = solve_triangle(a=5, b=5, A=120)
        self.assertIn("error", r)

    def test_right_triangle_boundary(self):
        # a == b*sin(A) → single right-triangle solution (B = 90°)
        # b=10, A=30°, a=5
        r = solve_triangle(a=5, b=10, A=30)
        self._check(r, a=5, b=10, A=30)
        self.assertTrue(approx(r["B"], 90.0, tol=1e-3))
        self.assertTrue(approx(r["C"], 60.0, tol=1e-3))


if __name__ == "__main__":
    unittest.main()
