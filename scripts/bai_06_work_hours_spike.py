import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

sys.stdout.reconfigure(encoding='utf-8')

# --- BÀI 6: Spike 40 giờ làm việc (gss2010.csv) ---

# 1. Đọc dữ liệu
gss = pd.read_csv("data/gss2010.csv")
hrs = gss["hrs1"].dropna()

total_n = len(hrs)
print("=== BÀI 6: TẦN SỐ VÀ TỈ LỆ LÀM VIỆC 39, 40, 41 GIỜ ===")
print(f"Tổng số phản hồi hợp lệ (N): {total_n}")

c39, c40, c41 = (hrs == 39).sum(), (hrs == 40).sum(), (hrs == 41).sum()
p39, p40, p41 = c39/total_n*100, c40/total_n*100, c41/total_n*100

print(f"Chính xác 39 giờ: {c39} ({p39:.2f}%)")
print(f"Chính xác 40 giờ: {c40} ({p40:.2f}%)")
print(f"Chính xác 41 giờ: {c41} ({p41:.2f}%)\n")

# 2. Vẽ 2 đồ thị histogram (bin width 1h và 5h)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
min_h, max_h = int(hrs.min()), int(hrs.max())

# Bin width = 1 giờ
bins1 = np.arange(min_h, max_h + 2, 1)
ax1.hist(hrs, bins=bins1, edgecolor='black', color='#4C72B0', alpha=0.85)
ax1.set_title('Histogram (Bin width = 1 hour)', fontweight='bold')
ax1.set_xlabel('Hours worked per week (hrs1)')
ax1.set_ylabel('Frequency')
ax1.grid(axis='y', linestyle='--', alpha=0.5)

# Bin width = 5 giờ
bins5 = np.arange(np.floor(min_h/5)*5, np.ceil(max_h/5)*5 + 6, 5)
ax2.hist(hrs, bins=bins5, edgecolor='black', color='#55A868', alpha=0.85)
ax2.set_title('Histogram (Bin width = 5 hours)', fontweight='bold')
ax2.set_xlabel('Hours worked per week (hrs1)')
ax2.set_ylabel('Frequency')
ax2.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig("output/bai_06_histograms.png", dpi=300)
print("Đã lưu biểu đồ: output/bai_06_histograms.png")
