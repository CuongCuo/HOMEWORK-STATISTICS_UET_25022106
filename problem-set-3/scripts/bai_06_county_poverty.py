import sys
from pathlib import Path
import pandas as pd
import numpy as np
from plotnine import (
    ggplot, aes, geom_histogram, facet_wrap, labs, theme_minimal, after_stat
)

sys.stdout.reconfigure(encoding='utf-8')

data_path = Path("data/county.csv")
if not data_path.exists():
    data_path = Path("../data/county.csv")

df = pd.read_csv(data_path)

# 1. Kích thước nhóm và thống kê mô tả
print("=== BÀI 6: COUNTY POVERTY & METRO ANALYSIS ===")
clean_df = df.dropna(subset=['poverty', 'metro']).copy()
counts = clean_df['metro'].value_counts()
print(f"Số lượng County trong nhóm Metro (yes): {counts.get('yes', 0)}")
print(f"Số lượng County trong nhóm Non-Metro (no): {counts.get('no', 0)}")
print(f"Tổng số County phân tích: {len(clean_df)}")

stats = clean_df.groupby('metro')['poverty'].agg(
    count='count',
    mean='mean',
    median='median',
    std='std',
    q25=lambda x: x.quantile(0.25),
    q75=lambda x: x.quantile(0.75)
).assign(iqr=lambda x: x['q75'] - x['q25'])
print("\nThống kê mô tả tỷ lệ nghèo (% poverty):")
print(stats.round(2))

# 2. Tạo biểu đồ so sánh: Số lượng (Count) vs Mật độ (Density)
p1 = (
    ggplot(clean_df, aes(x='poverty', fill='metro'))
    + geom_histogram(binwidth=2, color='white', alpha=0.7)
    + facet_wrap('~ metro', labeller=lambda s: f"Metro: {s}")
    + labs(
        title="Hình 1A: Tần suất thô (Count) theo nhóm Metro",
        x="Tỷ lệ nghèo (%)",
        y="Số lượng County",
        fill="Khu vực"
    )
    + theme_minimal()
)

p2 = (
    ggplot(clean_df, aes(x='poverty', y=after_stat('density'), fill='metro'))
    + geom_histogram(binwidth=2, color='white', alpha=0.7)
    + facet_wrap('~ metro', labeller=lambda s: f"Metro: {s}")
    + labs(
        title="Hình 1B: Mật độ phân phối (Density) chuẩn hóa theo nhóm Metro",
        x="Tỷ lệ nghèo (%)",
        y="Mật độ (Density)",
        fill="Khu vực"
    )
    + theme_minimal()
)

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

p1.save("output/bai_06_count.png", width=8, height=4, dpi=300)
p2.save("output/bai_06_histograms.png", width=8, height=4, dpi=300)
print("\nĐã lưu biểu đồ thành công vào thư mục output/")
