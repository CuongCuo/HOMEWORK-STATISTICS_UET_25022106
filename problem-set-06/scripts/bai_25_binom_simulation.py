import sys
from pathlib import Path
import numpy as np
from scipy.stats import binom
from plotnine import (
    ggplot, aes, geom_col, geom_step, geom_text, labs, theme_minimal,
    scale_x_continuous, scale_y_continuous, scale_fill_manual, facet_wrap
)
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

print("=== BÀI 25: MÔ PHỎNG TUNG ĐỒNG XU 4 LẦN - SO SÁNH THỰC NGHIỆM VỚI LÝ THUYẾT ===")

# Thông số
n = 4
p = 0.5
x_vals = np.arange(0, n + 1)
pmf_theory = binom.pmf(x_vals, n=n, p=p)
rng = np.random.default_rng(seed=2026)

# Mô phỏng 500 lần và 10_000 lần
sims = {500: None, 10_000: None}
for size in sims:
    samples = rng.binomial(n=n, p=p, size=size)
    freq = np.array([(samples == k).mean() for k in x_vals])
    sims[size] = freq

print("\nKết quả mô phỏng so với lý thuyết:\n")
header = f"{'k':>4} | {'Lý thuyết':>12} | {'500 lần':>12} | {'10 000 lần':>12}"
print(header)
print("-" * len(header))
for i, k in enumerate(x_vals):
    print(f"{k:>4} | {pmf_theory[i]:>12.4f} | {sims[500][i]:>12.4f} | {sims[10_000][i]:>12.4f}")

print("\nSai số tuyệt đối (|thực nghiệm - lý thuyết|):")
print(f"  500 lần   : max = {np.max(np.abs(sims[500] - pmf_theory)):.4f}, "
      f"mean = {np.mean(np.abs(sims[500] - pmf_theory)):.4f}")
print(f"  10 000 lần: max = {np.max(np.abs(sims[10_000] - pmf_theory)):.4f}, "
      f"mean = {np.mean(np.abs(sims[10_000] - pmf_theory)):.4f}")
print("\nNhận xét: Mô phỏng 10 000 lần cho tần suất sát lý thuyết hơn nhiều so với 500 lần")
print("         (Luật Số Lớn: tần suất hội tụ về xác suất khi số thí nghiệm tăng).")

# Tạo DataFrame để vẽ biểu đồ
rows = []
for k in x_vals:
    rows.append({'k': k, 'Tần suất': pmf_theory[k],   'Nhóm': 'Lý thuyết (Binomial)'})
    rows.append({'k': k, 'Tần suất': sims[500][k],    'Nhóm': 'Mô phỏng 500 lần'})
    rows.append({'k': k, 'Tần suất': sims[10_000][k], 'Nhóm': 'Mô phỏng 10 000 lần'})

df = pd.DataFrame(rows)

color_map = {
    'Lý thuyết (Binomial)': '#2C7BB6',
    'Mô phỏng 500 lần':     '#D7191C',
    'Mô phỏng 10 000 lần':  '#1A9641'
}

p_plot = (
    ggplot(df, aes(x='k', y='Tần suất', fill='Nhóm'))
    + geom_col(position='dodge', color='white', width=0.7)
    + facet_wrap('~ Nhóm', ncol=3)
    + scale_x_continuous(breaks=list(x_vals))
    + scale_y_continuous(limits=[0, 0.45])
    + scale_fill_manual(values=color_map)
    + labs(
        title="Bài 25: So sánh Tần suất Thực nghiệm với Phân phối Lý thuyết",
        subtitle="X ~ Binomial(n=4, p=0.5) – Tung đồng xu cân đối 4 lần",
        x="k (số mặt ngửa)",
        y="Tần suất / Xác suất",
        fill=""
    )
    + theme_minimal()
)

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

p_plot.save("output/bai_25_simulation.png", width=10, height=4.5, dpi=300)
print("\nĐã lưu biểu đồ thành công: output/bai_25_simulation.png")
