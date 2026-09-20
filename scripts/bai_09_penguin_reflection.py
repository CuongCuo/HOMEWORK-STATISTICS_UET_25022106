import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

sys.stdout.reconfigure(encoding='utf-8')

# --- BÀI 9: Cùng mean và SD, hình dạng vẫn có thể khác (Palmer Penguins) ---

# 1. Tải dữ liệu từ URL Palmer Penguins
url = "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv"
penguins = pd.read_csv(url)
x = penguins["body_mass_g"].dropna()

# 2. Tạo biến phản chiếu x_star = 2 * mean - x
x_bar = x.mean()
x_star = 2 * x_bar - x

def get_stats(series):
    m = series.mean()
    med = series.median()
    sd = series.std(ddof=1)
    q1, q3 = np.percentile(series, [25, 75])
    iqr = q3 - q1
    return m, med, sd, q1, q3, iqr

m_x, med_x, sd_x, q1_x, q3_x, iqr_x = get_stats(x)
m_xs, med_xs, sd_xs, q1_xs, q3_xs, iqr_xs = get_stats(x_star)

print("=== BÀI 9: THỐNG KÊ MÔ TẢ X VÀ X_STAR ===")
print(f"Dữ liệu gốc (x)     -> Mean: {m_x:.2f}, Median: {med_x:.2f}, SD: {sd_x:.2f}, IQR: {iqr_x:.2f}")
print(f"Phản chiếu (x_star) -> Mean: {m_xs:.2f}, Median: {med_xs:.2f}, SD: {sd_xs:.2f}, IQR: {iqr_xs:.2f}\n")

# 3. Vẽ 2 histogram so sánh cùng bin edges và trục ngang
min_val = min(x.min(), x_star.min())
max_val = max(x.max(), x_star.max())
bins = np.linspace(min_val, max_val, 25)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), sharex=True, sharey=True)

ax1.hist(x, bins=bins, edgecolor='black', color='#4C72B0', alpha=0.85)
ax1.set_title(f'Original x (body_mass_g)\nMean={m_x:.1f}, SD={sd_x:.1f} (Lệch phải)', fontweight='bold')
ax1.set_xlabel('Body Mass (g)')
ax1.set_ylabel('Frequency')
ax1.grid(axis='y', linestyle='--', alpha=0.5)

ax2.hist(x_star, bins=bins, edgecolor='black', color='#C44E52', alpha=0.85)
ax2.set_title(f'Reflected x_star (2*mean - x)\nMean={m_xs:.1f}, SD={sd_xs:.1f} (Lệch trái)', fontweight='bold')
ax2.set_xlabel('Body Mass (g)')
ax2.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig("output/bai_09_histograms.png", dpi=300)
print("Đã lưu biểu đồ: output/bai_09_histograms.png")
