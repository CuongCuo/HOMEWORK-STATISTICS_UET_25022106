import sys
from pathlib import Path
import pandas as pd
import numpy as np
from plotnine import (
    ggplot, aes, geom_col, facet_wrap, labs, theme_minimal
)

sys.stdout.reconfigure(encoding='utf-8')

data_path = Path("data/ncbirths.csv")
if not data_path.exists():
    data_path = Path("../data/ncbirths.csv")

df = pd.read_csv(data_path)

print("=== BÀI 10: SỐ CA SINH NON VS NGUY CƠ SINH NON (NCBIRTHS) ===")
clean_df = df.dropna(subset=['mage', 'premie']).copy()

# Tạo nhóm tuổi 5 năm cho tuổi mẹ (mage)
bins = [10, 15, 20, 25, 30, 35, 40, 45, 50]
labels = ["10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49"]
clean_df['age_group'] = pd.cut(clean_df['mage'], bins=bins, labels=labels, right=False)

# Thống kê tổng ca sinh và ca sinh non theo nhóm tuổi
summary = clean_df.groupby('age_group', observed=False).agg(
    total_births=('premie', 'count'),
    premie_count=('premie', lambda x: (x == 'premie').sum())
).reset_index()

summary['premie_rate'] = (summary['premie_count'] / summary['total_births']) * 100

print("\nBảng tổng hợp theo nhóm tuổi mẹ (Mage Age Groups):")
print(summary.round(2).to_string(index=False))

# Đồ thị so sánh: Số ca sinh non (Premie Count) vs Tỷ lệ sinh non (Premie Rate)
plot_data = pd.melt(
    summary,
    id_vars=['age_group'],
    value_vars=['premie_count', 'premie_rate'],
    var_name='Metric',
    value_name='Value'
)

metric_labels = {
    'premie_count': '1. Số ca sinh non (Số lượng thô)',
    'premie_rate': '2. Tỷ lệ sinh non (% nguy cơ thực tế)'
}
plot_data['Metric_Name'] = plot_data['Metric'].map(metric_labels)

p = (
    ggplot(plot_data, aes(x='age_group', y='Value', fill='Metric'))
    + geom_col(show_legend=False)
    + facet_wrap('~ Metric_Name', scales='free_y', ncol=2)
    + labs(
        title="So sánh Số ca Sinh non (Count) và Tỷ lệ Sinh non (Risk Rate)",
        x="Nhóm tuổi mẹ (Mage)",
        y="Giá trị"
    )
    + theme_minimal()
)

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)
p.save("output/bai_10_histograms.png", width=9, height=4.5, dpi=300)
print("\nĐã lưu biểu đồ thành công: output/bai_10_histograms.png")
