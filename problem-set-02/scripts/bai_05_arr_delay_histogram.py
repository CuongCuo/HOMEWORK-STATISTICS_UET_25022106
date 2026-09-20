import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import sys

sys.stdout.reconfigure(encoding='utf-8')

# --- BÀI 5: Histogram arr_delay (nycflights.csv) ---

# 1. Đọc dữ liệu và lọc arr_delay trong khoảng [-30, 150)
flights = pd.read_csv("data/nycflights.csv")
x = flights["arr_delay"].dropna()
x = x[(x >= -30) & (x < 150)]

# 2. Tính 4 đại lượng tóm tắt
mean_val = x.mean()
median_val = x.median()
std_val = x.std(ddof=1)
q25, q75 = np.percentile(x, [25, 75])
iqr_val = q75 - q25

print("=== BÀI 5: ĐẠI LƯỢNG TÓM TẮT DỮ LIỆU GỐC ===")
print(f"Mean: {mean_val:.2f} phút")
print(f"Median: {median_val:.2f} phút")
print(f"Sample SD: {std_val:.2f} phút")
print(f"IQR: {iqr_val:.2f} phút\n")

# 3. Vẽ 4 đồ thị histogram với bin width = 5, 15, 30, 60
bin_widths = [5, 15, 30, 60]
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes = axes.flatten()

for idx, bw in enumerate(bin_widths):
    bins = np.arange(-30, 150 + bw, bw)
    ax = axes[idx]
    ax.hist(x, bins=bins, edgecolor='black', color='#4C72B0', alpha=0.85)
    ax.set_title(f'Histogram (Bin width = {bw} min)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Arrival Delay (minutes)', fontsize=10)
    ax.set_ylabel('Frequency', fontsize=10)
    ax.set_xlim([-30, 150])
    ax.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig("output/bai_05_histograms.png", dpi=300)
print("Đã lưu biểu đồ: output/bai_05_histograms.png")
