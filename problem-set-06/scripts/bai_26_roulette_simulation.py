import sys
from pathlib import Path
import numpy as np
from scipy.stats import binom
from plotnine import (
    ggplot, aes, geom_histogram, geom_vline, labs, theme_minimal, after_stat, annotate
)
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

print("=== BÀI 26: MÔ PHỎNG ROULETTE MỸ - XÁC SUẤT ≥55 Ô ĐỎ TRONG 100 LƯỢT ===")

# Thông số roulette kiểu Mỹ
n_spins = 100          # số lượt quay mỗi thí nghiệm
p_red   = 18 / 38     # xác suất ô đỏ mỗi lượt
threshold = 55         # ngưỡng cần kiểm tra
n_sim   = 10_000       # số thí nghiệm mô phỏng

print(f"\nThông số:")
print(f"  Số lượt quay: n = {n_spins}")
print(f"  Xác suất ô đỏ: p = 18/38 ≈ {p_red:.6f}")
print(f"  X ~ Binomial(n={n_spins}, p=18/38)")

# Xác suất lý thuyết P(X >= 55)
prob_theory = 1 - binom.cdf(threshold - 1, n=n_spins, p=p_red)
print(f"\n--- XÁC SUẤT LÝ THUYẾT ---")
print(f"P(X ≥ {threshold}) = 1 - P(X ≤ {threshold-1})")
print(f"             = 1 - {binom.cdf(threshold-1, n_spins, p_red):.6f}")
print(f"             = {prob_theory:.6f}")
print(f"             ≈ {prob_theory*100:.4f}%")

# Kỳ vọng và độ lệch chuẩn của X
mean_X = n_spins * p_red
std_X  = np.sqrt(n_spins * p_red * (1 - p_red))
print(f"\nKỳ vọng E[X] = n*p = {mean_X:.4f}")
print(f"Độ lệch chuẩn σ = {std_X:.4f}")
print(f"Ngưỡng 55 cách kỳ vọng: {(threshold - mean_X)/std_X:.2f} độ lệch chuẩn")

# Mô phỏng 10 000 thí nghiệm
rng = np.random.default_rng(seed=2026)
samples = rng.binomial(n=n_spins, p=p_red, size=n_sim)
freq_empirical = (samples >= threshold).mean()

print(f"\n--- KẾT QUẢ MÔ PHỎNG ({n_sim:,} thí nghiệm) ---")
print(f"Số thí nghiệm có X ≥ {threshold}: {(samples >= threshold).sum()}")
print(f"Tần suất thực nghiệm P̂(X ≥ {threshold}) = {freq_empirical:.6f}")
print(f"\nSo sánh:")
print(f"  Lý thuyết  : {prob_theory:.6f} ({prob_theory*100:.4f}%)")
print(f"  Thực nghiệm: {freq_empirical:.6f} ({freq_empirical*100:.4f}%)")
print(f"  Sai số tuyệt đối: {abs(freq_empirical - prob_theory):.6f}")

# Thống kê mô tả của mô phỏng
print(f"\nThống kê mô tả X (10 000 mô phỏng):")
print(f"  Min: {samples.min()}, Max: {samples.max()}")
print(f"  Mean: {samples.mean():.4f} (lý thuyết: {mean_X:.4f})")
print(f"  Std : {samples.std():.4f} (lý thuyết: {std_X:.4f})")

# Vẽ biểu đồ phân phối mô phỏng
df = pd.DataFrame({'X': samples})

p_plot = (
    ggplot(df, aes(x='X'))
    + geom_histogram(binwidth=1, fill='#4C72B0', color='white', alpha=0.8)
    + geom_vline(xintercept=threshold - 0.5, color='red', linetype='dashed', size=1)
    + annotate('text', x=threshold + 1.5, y=600,
               label=f'Vùng X ≥ {threshold}\nLT: {prob_theory:.4f}\nTN: {freq_empirical:.4f}',
               ha='left', size=9, color='red')
    + labs(
        title=f"Bài 26: Phân phối Mô phỏng – Số Lượt Đỏ trong {n_spins} Lượt Roulette",
        subtitle=f"X ~ Binomial(n=100, p=18/38), {n_sim:,} thí nghiệm mô phỏng",
        x="Số lượt ô đỏ (X)",
        y="Số lần xuất hiện"
    )
    + theme_minimal()
)

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

p_plot.save("output/bai_26_roulette.png", width=9, height=5, dpi=300)
print("\nĐã lưu biểu đồ thành công: output/bai_26_roulette.png")
