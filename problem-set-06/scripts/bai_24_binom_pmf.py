import sys
from pathlib import Path
import numpy as np
from scipy.stats import binom
from plotnine import (
    ggplot, aes, geom_col, geom_text, labs, theme_minimal, scale_x_continuous, scale_y_continuous
)
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

print("=== BÀI 24: HÀM KHỐI XÁC SUẤT - TUNG ĐỒNG XU 4 LẦN (SCIPY BINOM) ===")

# Thông số phân phối nhị thức
n = 4      # số lần tung
p = 0.5    # xác suất xuất hiện mặt ngửa (đồng xu cân đối)

print(f"\nPhân phối: X ~ Binomial(n={n}, p={p})")
print(f"X = số mặt ngửa khi tung đồng xu cân đối {n} lần")

# Tính PMF cho tất cả các giá trị x = 0, 1, 2, 3, 4
x_vals = np.arange(0, n + 1)
pmf_vals = binom.pmf(x_vals, n=n, p=p)

print("\nHàm khối xác suất P(X = k):")
print(f"{'k':>4} | {'P(X=k)':>10} | {'P(X=k) phân số':>16}")
print("-" * 36)
fractions = ["1/16", "4/16 = 1/4", "6/16 = 3/8", "4/16 = 1/4", "1/16"]
for k, prob, frac in zip(x_vals, pmf_vals, fractions):
    print(f"{k:>4} | {prob:>10.4f} | {frac:>16}")

print(f"\nKiểm tra tổng xác suất: Sum P(X=k) = {pmf_vals.sum():.6f} (phải = 1.0)")

# Các xác suất cộng dồn
print("\nHàm phân phối tích lũy F(k) = P(X ≤ k):")
for k in x_vals:
    print(f"  P(X ≤ {k}) = {binom.cdf(k, n=n, p=p):.4f}")

# Kỳ vọng và phương sai
mean_val = binom.mean(n, p)
var_val  = binom.var(n, p)
std_val  = binom.std(n, p)
print(f"\nKỳ vọng:   E[X] = n*p = {n}*{p} = {mean_val}")
print(f"Phương sai: Var(X) = n*p*(1-p) = {n}*{p}*{1-p} = {var_val}")
print(f"Độ lệch chuẩn: σ = {std_val:.4f}")

# Vẽ biểu đồ PMF
df = pd.DataFrame({'k': x_vals, 'PMF': pmf_vals})
df['label'] = df['PMF'].apply(lambda v: f"{v:.4f}")

p_plot = (
    ggplot(df, aes(x='k', y='PMF'))
    + geom_col(fill='#4C72B0', color='white', width=0.6)
    + geom_text(aes(label='label'), va='bottom', nudge_y=0.005, size=9)
    + scale_x_continuous(breaks=list(x_vals), labels=[str(k) for k in x_vals])
    + scale_y_continuous(limits=[0, 0.45])
    + labs(
        title="Bài 24: Hàm Khối Xác Suất – X ~ Binomial(n=4, p=0.5)",
        subtitle="X = số mặt ngửa khi tung đồng xu cân đối 4 lần",
        x="k (số mặt ngửa)",
        y="P(X = k)"
    )
    + theme_minimal()
)

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

p_plot.save("output/bai_24_pmf.png", width=7, height=5, dpi=300)
print("\nĐã lưu biểu đồ thành công: output/bai_24_pmf.png")
