import sys
from pathlib import Path
import pandas as pd
import numpy as np
from plotnine import (
    ggplot, aes, geom_boxplot, geom_bar, facet_wrap, labs, theme_minimal, position_fill
)

sys.stdout.reconfigure(encoding='utf-8')

data_path = Path("data/loans_full_schema.csv")
if not data_path.exists():
    data_path = Path("../data/loans_full_schema.csv")

df = pd.read_csv(data_path)

print("=== BÀI 9: LÃI SUẤT VÀ SỞ HỮU NHÀ (LOANS FULL SCHEMA) ===")
clean_df = df.dropna(subset=['interest_rate', 'grade', 'homeownership']).copy()
clean_df['homeownership_cat'] = clean_df['homeownership'].apply(
    lambda x: 'RENT' if x == 'RENT' else ('MORTGAGE/OWN' if x in ['MORTGAGE', 'OWN'] else 'OTHER')
)
clean_df = clean_df[clean_df['homeownership_cat'] != 'OTHER']

# 1. Phân phối biên của interest_rate theo homeownership
marginal_stats = clean_df.groupby('homeownership_cat')['interest_rate'].agg(['count', 'mean', 'median', 'std'])
print("\n1. Phân phối BIÊN của lãi suất (% interest_rate) theo sở hữu nhà:")
print(marginal_stats.round(2))

# 2. Điều kiện hóa theo grade
conditional_stats = clean_df.groupby(['grade', 'homeownership_cat'])['interest_rate'].agg(['count', 'mean', 'median'])
print("\n2. Phân phối CÓ ĐIỀU KIỆN theo Grade:")
print(conditional_stats.round(2))

# 3. Phân bố Grade theo sở hữu nhà (Trọng số nhóm)
grade_dist = pd.crosstab(clean_df['homeownership_cat'], clean_df['grade'], normalize='index') * 100
print("\n3. Phân bố % Grade trong từng nhóm sở hữu nhà (Cơ cấu nhóm):")
print(grade_dist.round(2))

# Biểu đồ 1: Boxplot Lãi suất theo Grade và Homeownership
p1 = (
    ggplot(clean_df, aes(x='grade', y='interest_rate', fill='homeownership_cat'))
    + geom_boxplot(alpha=0.7)
    + labs(
        title="Lãi suất (Interest Rate) theo Grade và Sở hữu nhà",
        x="Xếp hạng rủi ro (Grade)",
        y="Lãi suất (%)",
        fill="Sở hữu nhà"
    )
    + theme_minimal()
)

# Biểu đồ 2: Cơ cấu Grade theo Homeownership
p2 = (
    ggplot(clean_df, aes(x='homeownership_cat', fill='grade'))
    + geom_bar(position=position_fill())
    + labs(
        title="Tỷ lệ cơ cấu Grade theo nhóm Sở hữu nhà",
        x="Trạng thái sở hữu nhà",
        y="Tỷ lệ phần trăm (Proportion)",
        fill="Grade"
    )
    + theme_minimal()
)

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)
p1.save("output/bai_09_histograms.png", width=8, height=4.5, dpi=300)
p2.save("output/bai_09_grade_dist.png", width=7, height=4.5, dpi=300)
print("\nĐã lưu biểu đồ thành công: output/bai_09_histograms.png và output/bai_09_grade_dist.png")
