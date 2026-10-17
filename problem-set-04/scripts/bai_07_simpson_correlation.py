import sys
import pandas as pd
from plotnine import (
    ggplot, aes, geom_point, geom_smooth, labs, theme_minimal
)

sys.stdout.reconfigure(encoding='utf-8')

print("=== BÀI 7: TƯƠNG QUAN ÂM DỰA TRÊN 3 TƯƠNG QUAN DƯƠNG (SIMPSON'S PARADOX) ===")

from plotnine.data import penguins

clean_df = penguins.dropna(subset=['bill_length_mm', 'bill_depth_mm', 'species']).copy()

r_all = clean_df['bill_length_mm'].corr(clean_df['bill_depth_mm'])
print(f"Tương quan toàn bộ r_all = {r_all:.3f}")

r_by_species = clean_df.groupby('species').apply(
    lambda df: df['bill_length_mm'].corr(df['bill_depth_mm']), include_groups=False
)
print("\nTương quan theo từng loài:")
for sp, r_val in r_by_species.items():
    print(f"Loài {sp}: r = {r_val:+.3f}")

p = (
    ggplot(clean_df, aes(x='bill_length_mm', y='bill_depth_mm', color='species'))
    + geom_point(alpha=0.7)
    + geom_smooth(method='lm', se=False)
    + geom_smooth(aes(group=1), method='lm', color='black', linetype='dashed', se=False)
    + labs(
        title="Nghịch lý Simpson: Tương quan giữa Mỏ dài và Mỏ sâu (Penguins)",
        subtitle="Đường đen nét đứt: Hồi quy gộp (r = -0.235). Đường màu: Hồi quy theo loài (r > 0)",
        x="Bill Length (mm)",
        y="Bill Depth (mm)",
        color="Loài"
    )
    + theme_minimal()
)

p.save("output/bai_07_simpson.png", width=8, height=5, dpi=300)
print("\nĐã lưu biểu đồ: output/bai_07_simpson.png")
