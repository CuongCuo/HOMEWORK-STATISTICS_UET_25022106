import sys
import math
from pathlib import Path
import numpy as np
from scipy.stats import hypergeom
from plotnine import (
    ggplot, aes, geom_col, geom_text, labs, theme_minimal,
    scale_x_continuous, scale_y_continuous, scale_fill_manual, facet_wrap
)
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

print("=== BÀI 27: PHÂN TÍCH MÃ HYPERGEOMETRIC - XÁC ĐỊNH ĐÚNG/SAI ===")

print("""
Bài toán: Mô phỏng số sản phẩm KHÔNG ĐẠT CHUẨN khi chọn ngẫu nhiên 5 sản phẩm
          KHÔNG HOÀN LẠI từ lô 20 sản phẩm gồm 6 sản phẩm không đạt chuẩn.

Hai đoạn mã đề bài:
  x1 = hypergeom.rvs(M=20, n=6,  N=5, size=10_000, random_state=2026)
  x2 = hypergeom.rvs(M=20, n=14, N=5, size=10_000, random_state=2026)
""")

print("--- GIẢI THÍCH CÁC THAM SỐ CỦA hypergeom.rvs ---")
print("""
  M = Tổng số phần tử trong lô (population size)       → M = 20
  n = Số phần tử thuộc loại "thành công" (success type) trong lô
      → tức là số sản phẩm KHÔNG ĐẠT CHUẨN = 6
  N = Số lần rút (số sản phẩm được chọn, sample size)  → N = 5
  X = Số phần tử thuộc loại "thành công" được rút ra   → X = số sản phẩm không đạt được chọn
""")

print("--- PHÂN TÍCH ĐOẠN MÃ ĐÚNG/SAI ---")
print("""
  x1: hypergeom.rvs(M=20, n=6,  N=5, ...)
      → n=6 là số sản phẩm KHÔNG ĐẠT CHUẨN
      → X ~ HyperGeometric(M=20, n=6, N=5)
      → ĐÂY LÀ ĐOẠN MÃ ĐÚNG ✓

  x2: hypergeom.rvs(M=20, n=14, N=5, ...)
      → n=14 là số sản phẩm ĐẠT CHUẨN (20 - 6 = 14)
      → X ~ HyperGeometric(M=20, n=14, N=5)
      → X sẽ đếm số sản phẩm ĐẠT CHUẨN được chọn (sai mục tiêu) ✗
      → ĐÂY LÀ ĐOẠN MÃ SAI ✗
""")

print("--- SỬA ĐOẠN MÃ SAI ---")
print("  Đoạn mã đúng: hypergeom.rvs(M=20, n=6, N=5, size=10_000, random_state=2026)")
print("  (Cần thay n=14 bằng n=6)")

# Thực thi đoạn mã đúng
x1 = hypergeom.rvs(M=20, n=6,  N=5, size=10_000, random_state=2026)
x2_wrong = hypergeom.rvs(M=20, n=14, N=5, size=10_000, random_state=2026)
x2_fixed = hypergeom.rvs(M=20, n=6,  N=5, size=10_000, random_state=2025)  # đã sửa

# Xác suất lý thuyết P(X = 2) từ phân phối siêu bội
prob_X2_theory = hypergeom.pmf(2, M=20, n=6, N=5)
prob_X2_empirical = (x1 == 2).mean()

print(f"\n--- ƯỚC LƯỢNG P(X = 2) ---")
print(f"\nXác suất lý thuyết (siêu bội): P(X=2) = C(6,2)*C(14,3)/C(20,5)")
print(f"  = {math.comb(6,2)} * {math.comb(14,3)} / {math.comb(20,5)}")
print(f"  = {math.comb(6,2) * math.comb(14,3)} / {math.comb(20,5)}")
print(f"  = {prob_X2_theory:.6f}")
print(f"\nTần suất thực nghiệm (10 000 mô phỏng, mã đúng x1):")
print(f"  P̂(X=2) = {prob_X2_empirical:.6f}")
print(f"\nSai số tuyệt đối: {abs(prob_X2_empirical - prob_X2_theory):.6f}")

# Phân phối đầy đủ
print("\nHàm khối xác suất đầy đủ X ~ HyperGeometric(M=20, n=6, N=5):")
print(f"{'k':>4} | {'Lý thuyết':>12} | {'Thực nghiệm x1':>16}")
print("-" * 38)
for k in range(0, 6):
    th = hypergeom.pmf(k, M=20, n=6, N=5)
    em = (x1 == k).mean()
    print(f"{k:>4} | {th:>12.6f} | {em:>16.6f}")

# Vẽ biểu đồ so sánh đúng/sai và lý thuyết
rows = []
for k in range(0, 6):
    rows.append({'k': k, 'Xác suất': hypergeom.pmf(k, 20, 6, 5),  'Loại': '1. Lý thuyết HyperGeom'})
    rows.append({'k': k, 'Xác suất': (x1 == k).mean(),             'Loại': '2. Mô phỏng đúng (n=6)'})
    rows.append({'k': k, 'Xác suất': (x2_wrong == k).mean(),       'Loại': '3. Mô phỏng sai (n=14)'})

df = pd.DataFrame(rows)

color_map = {
    '1. Lý thuyết HyperGeom':  '#2C7BB6',
    '2. Mô phỏng đúng (n=6)':  '#1A9641',
    '3. Mô phỏng sai (n=14)':  '#D7191C',
}

p_plot = (
    ggplot(df, aes(x='k', y='Xác suất', fill='Loại'))
    + geom_col(position='dodge', color='white', width=0.75)
    + facet_wrap('~ Loại', ncol=3)
    + scale_x_continuous(breaks=list(range(6)))
    + scale_fill_manual(values=color_map)
    + labs(
        title="Bài 27: So sánh Mô phỏng Đúng/Sai – X ~ HyperGeometric(M=20, n=6, N=5)",
        subtitle="Mã sai (n=14) đếm sản phẩm ĐẠT CHUẨN thay vì sản phẩm KHÔNG ĐẠT CHUẨN",
        x="k (số sản phẩm không đạt chuẩn được chọn)",
        y="Xác suất / Tần suất",
        fill=""
    )
    + theme_minimal()
)

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

p_plot.save("output/bai_27_hypergeom.png", width=10, height=4.5, dpi=300)
print("\nĐã lưu biểu đồ thành công: output/bai_27_hypergeom.png")
