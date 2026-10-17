import sys
from pathlib import Path
import pandas as pd
import numpy as np
from plotnine import (
    ggplot, aes, geom_bar, geom_hline, facet_wrap, labs, theme_minimal, after_stat
)

sys.stdout.reconfigure(encoding='utf-8')

data_path = Path("data/run10.csv")
if not data_path.exists():
    data_path = Path("../data/run10.csv")

df = pd.read_csv(data_path)

print("=== BÀI 7: HEAPING Ở CHỮ SỐ CUỐI (RUN10 AGE) ===")
clean_df = df.dropna(subset=['age']).copy()
clean_df['last_digit'] = (clean_df['age'] % 10).astype(int)

# Tỷ lệ cho từng chữ số 0-9
digit_counts = clean_df['last_digit'].value_counts(normalize=True).sort_index() * 100
print("\nTỷ lệ % xuất hiện của từng chữ số cuối (0-9):")
for digit, prop in digit_counts.items():
    print(f"Chữ số {digit}: {prop:.2f}%")

p_0_5 = digit_counts.get(0, 0) + digit_counts.get(5, 0)
print(f"\nTổng tỷ lệ tuổi kết thúc bằng 0 hoặc 5: {p_0_5:.2f}% (Tham chiếu đều: 20.00%)")

# Điều kiện hóa theo giới tính (gender)
clean_df['gender'] = clean_df['gender'].astype(str)
gender_digit_counts = clean_df.groupby(['gender', 'last_digit']).size().unstack(fill_value=0)
gender_digit_props = (gender_digit_counts.T / gender_digit_counts.sum(axis=1)).T * 100
print("\nTỷ lệ % chữ số cuối theo Giới tính:")
print(gender_digit_props.round(2))

# Biểu đồ tỉ lệ chữ số cuối theo giới tính
clean_df['last_digit_cat'] = clean_df['last_digit'].astype(str)

p = (
    ggplot(clean_df, aes(x='last_digit_cat', fill='gender'))
    + geom_bar(aes(y=after_stat('prop * 100'), group='gender'), show_legend=False)
    + geom_hline(yintercept=10, color='red', linetype='dashed', size=1)
    + facet_wrap('~ gender', labeller=lambda g: f"Giới tính: {g}")
    + labs(
        title="Tỷ lệ % chữ số cuối của Tuổi người chạy (Run10)",
        subtitle="Đường nét đứt đỏ (10%) thể hiện mốc phân bố đều tham chiếu",
        x="Chữ số cuối (Age % 10)",
        y="Tỷ lệ phần trăm (%)"
    )
    + theme_minimal()
)

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)
p.save("output/bai_07_histograms.png", width=8, height=4, dpi=300)
print("\nĐã lưu biểu đồ thành công: output/bai_07_histograms.png")
