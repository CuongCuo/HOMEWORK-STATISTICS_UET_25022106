import sys
import math
from pathlib import Path
import numpy as np
from scipy.stats import binom, hypergeom, poisson
from plotnine import (
    ggplot, aes, geom_col, geom_point, geom_line, labs, theme_minimal,
    scale_x_continuous, scale_fill_manual, facet_wrap
)
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

print("=== BÀI 28: SO SÁNH BA PHÂN PHỐI RỜI RẠC – SCIPY + MÔ PHỎNG 10 000 LẦN ===")

rng = np.random.default_rng(seed=2026)
N_SIM = 10_000

# ==============================================================
# Trường hợp 1: Binomial(n=20, p=0.9) – số sản phẩm ĐẠT CHUẨN
# ==============================================================
print("\n" + "=" * 60)
print("TRƯỜNG HỢP 1: X ~ Binomial(n=20, p=0.9)")
print("Ý nghĩa: Số sản phẩm ĐẠT CHUẨN trong 20 sản phẩm (p=0.9)")
print("=" * 60)

n1, p1 = 20, 0.9
x1_theory_k = 18  # xác suất lý thuyết chọn P(X = 18)

x1_pmf = binom.pmf(x1_theory_k, n=n1, p=p1)
x1_cdf = binom.cdf(x1_theory_k, n=n1, p=p1)
print(f"\nHàm khối xác suất P(X = {x1_theory_k}) = {x1_pmf:.6f}")
print(f"Hàm phân phối tích lũy F({x1_theory_k}) = P(X ≤ {x1_theory_k}) = {x1_cdf:.6f}")
print(f"Kỳ vọng E[X] = np = {n1*p1}, Phương sai Var(X) = np(1-p) = {n1*p1*(1-p1):.4f}")

sim1 = rng.binomial(n=n1, p=p1, size=N_SIM)
freq1 = (sim1 == x1_theory_k).mean()
print(f"\nMô phỏng {N_SIM:,} lần: Tần suất P̂(X={x1_theory_k}) = {freq1:.6f}")
print(f"Sai số tuyệt đối: {abs(freq1 - x1_pmf):.6f}")

# Phân phối đầy đủ (PMF từ 12 đến 20)
print("\nPMF từ k=12 đến 20:")
print(f"{'k':>4} | {'P(X=k) lý thuyết':>18} | {'Tần suất TN':>14}")
print("-" * 42)
for k in range(12, n1 + 1):
    th = binom.pmf(k, n1, p1)
    em = (sim1 == k).mean()
    print(f"{k:>4} | {th:>18.6f} | {em:>14.6f}")

# ==============================================================
# Trường hợp 2: Hypergeometric(M=20, n=6, N=5) – không đạt chuẩn
# ==============================================================
print("\n" + "=" * 60)
print("TRƯỜNG HỢP 2: X ~ HyperGeometric(M=20, n=6, N=5)")
print("Ý nghĩa: Số sản phẩm KHÔNG ĐẠT CHUẨN khi chọn 5 từ lô 20 (6 lỗi)")
print("=" * 60)

M2, n2_hyp, N2 = 20, 6, 5
x2_theory_k = 1  # xác suất lý thuyết chọn P(X = 1)

x2_pmf = hypergeom.pmf(x2_theory_k, M=M2, n=n2_hyp, N=N2)
x2_cdf = hypergeom.cdf(x2_theory_k, M=M2, n=n2_hyp, N=N2)
print(f"\nHàm khối xác suất P(X = {x2_theory_k}) = C(6,1)*C(14,4)/C(20,5)")
print(f"  = {math.comb(6,1)} * {math.comb(14,4)} / {math.comb(20,5)} = {x2_pmf:.6f}")
print(f"Hàm phân phối tích lũy F({x2_theory_k}) = P(X ≤ {x2_theory_k}) = {x2_cdf:.6f}")

kmax2 = min(n2_hyp, N2)
x2_mean = N2 * n2_hyp / M2
x2_var  = N2 * (n2_hyp/M2) * ((M2-n2_hyp)/M2) * ((M2-N2)/(M2-1))
print(f"Kỳ vọng E[X] = N*n/M = {N2}*{n2_hyp}/{M2} = {x2_mean:.4f}")
print(f"Phương sai Var(X) = {x2_var:.6f}")

sim2 = hypergeom.rvs(M=M2, n=n2_hyp, N=N2, size=N_SIM, random_state=2026)
freq2 = (sim2 == x2_theory_k).mean()
print(f"\nMô phỏng {N_SIM:,} lần: Tần suất P̂(X={x2_theory_k}) = {freq2:.6f}")
print(f"Sai số tuyệt đối: {abs(freq2 - x2_pmf):.6f}")

print("\nPMF đầy đủ:")
print(f"{'k':>4} | {'P(X=k) lý thuyết':>18} | {'Tần suất TN':>14}")
print("-" * 42)
for k in range(0, kmax2 + 1):
    th = hypergeom.pmf(k, M2, n2_hyp, N2)
    em = (sim2 == k).mean()
    print(f"{k:>4} | {th:>18.6f} | {em:>14.6f}")

# ==============================================================
# Trường hợp 3: Poisson(λ=4) – số yêu cầu đến máy chủ
# ==============================================================
print("\n" + "=" * 60)
print("TRƯỜNG HỢP 3: X ~ Poisson(λ=4)")
print("Ý nghĩa: Số yêu cầu đến máy chủ trong một phút (λ=4)")
print("=" * 60)

lam3 = 4
x3_theory_k = 3  # xác suất lý thuyết chọn P(X = 3)

x3_pmf = poisson.pmf(x3_theory_k, mu=lam3)
x3_cdf = poisson.cdf(x3_theory_k, mu=lam3)
print(f"\nHàm khối xác suất P(X = {x3_theory_k}) = e^(-{lam3}) * {lam3}^{x3_theory_k} / {x3_theory_k}!")
print(f"  = {x3_pmf:.6f}")
print(f"Hàm phân phối tích lũy F({x3_theory_k}) = P(X ≤ {x3_theory_k}) = {x3_cdf:.6f}")
print(f"Kỳ vọng E[X] = λ = {lam3}, Phương sai Var(X) = λ = {lam3}")

sim3 = rng.poisson(lam=lam3, size=N_SIM)
freq3 = (sim3 == x3_theory_k).mean()
print(f"\nMô phỏng {N_SIM:,} lần: Tần suất P̂(X={x3_theory_k}) = {freq3:.6f}")
print(f"Sai số tuyệt đối: {abs(freq3 - x3_pmf):.6f}")

print("\nPMF từ k=0 đến 10:")
print(f"{'k':>4} | {'P(X=k) lý thuyết':>18} | {'Tần suất TN':>14}")
print("-" * 42)
for k in range(0, 11):
    th = poisson.pmf(k, lam3)
    em = (sim3 == k).mean()
    print(f"{k:>4} | {th:>18.6f} | {em:>14.6f}")

# ==============================================================
# BẢNG TỔNG HỢP
# ==============================================================
print("\n" + "=" * 70)
print("BẢNG TỔNG HỢP – SO SÁNH LÝ THUYẾT VÀ THỰC NGHIỆM")
print("=" * 70)
summary = pd.DataFrame({
    'Phân phối': [
        'Binomial(n=20, p=0.9)',
        'HyperGeometric(M=20, n=6, N=5)',
        'Poisson(λ=4)'
    ],
    'Tham số': [
        'n=20, p=0.9',
        'M=20, n=6, N=5',
        'λ=4'
    ],
    'Xác suất chọn': [
        f'P(X={x1_theory_k})',
        f'P(X={x2_theory_k})',
        f'P(X={x3_theory_k})'
    ],
    'Lý thuyết': [
        round(x1_pmf, 6),
        round(x2_pmf, 6),
        round(x3_pmf, 6)
    ],
    'Thực nghiệm': [
        round(freq1, 6),
        round(freq2, 6),
        round(freq3, 6)
    ],
    'Sai số |TN-LT|': [
        round(abs(freq1 - x1_pmf), 6),
        round(abs(freq2 - x2_pmf), 6),
        round(abs(freq3 - x3_pmf), 6)
    ]
})
print(summary.to_string(index=False))

# ==============================================================
# VẼ BIỂU ĐỒ SO SÁNH BA PHÂN PHỐI
# ==============================================================
rows = []

# Case 1: Binomial (chỉ vẽ k từ 10 đến 20)
for k in range(10, 21):
    rows.append({'k': k, 'Xác suất': binom.pmf(k, n1, p1),   'Loại': 'theory', 'Phân phối': '1. Binomial(20, 0.9)'})
    rows.append({'k': k, 'Xác suất': (sim1 == k).mean(),     'Loại': 'empirical', 'Phân phối': '1. Binomial(20, 0.9)'})

# Case 2: Hypergeometric
for k in range(0, kmax2 + 1):
    rows.append({'k': k, 'Xác suất': hypergeom.pmf(k, M2, n2_hyp, N2), 'Loại': 'theory', 'Phân phối': '2. HyperGeom(20,6,5)'})
    rows.append({'k': k, 'Xác suất': (sim2 == k).mean(),                'Loại': 'empirical', 'Phân phối': '2. HyperGeom(20,6,5)'})

# Case 3: Poisson
for k in range(0, 13):
    rows.append({'k': k, 'Xác suất': poisson.pmf(k, lam3), 'Loại': 'theory', 'Phân phối': '3. Poisson(λ=4)'})
    rows.append({'k': k, 'Xác suất': (sim3 == k).mean(),   'Loại': 'empirical', 'Phân phối': '3. Poisson(λ=4)'})

df_all = pd.DataFrame(rows)

color_map = {'theory': '#2C7BB6', 'empirical': '#D7191C'}

p_plot = (
    ggplot(df_all, aes(x='k', y='Xác suất', fill='Loại'))
    + geom_col(position='dodge', color='white', width=0.7, alpha=0.85)
    + facet_wrap('~ Phân phối', scales='free', ncol=3)
    + scale_fill_manual(values=color_map, labels=['Lý thuyết', 'Thực nghiệm (10k)'])
    + labs(
        title="Bài 28: So sánh PMF Lý thuyết và Tần suất Thực nghiệm (10 000 mô phỏng)",
        subtitle="Ba phân phối rời rạc: Binomial, HyperGeometric, Poisson",
        x="k",
        y="Xác suất / Tần suất",
        fill=""
    )
    + theme_minimal()
)

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

p_plot.save("output/bai_28_three_distributions.png", width=13, height=5, dpi=300)
print("\nĐã lưu biểu đồ thành công: output/bai_28_three_distributions.png")
