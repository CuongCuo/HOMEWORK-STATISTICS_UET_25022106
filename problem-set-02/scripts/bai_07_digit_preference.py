import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

# --- BÀI 7: Con người có báo cáo số tròn không? (gpa_study_hours.csv) ---

# 1. Đọc dữ liệu
study = pd.read_csv("data/gpa_study_hours.csv")
h = study["study_hours"].dropna()

print("=== BÀI 7: BẢNG TẦN SỐ CHỮ SỐ HÀNG ĐƠN VỊ ===")
last_digits = (h.astype(int) % 10)
freq_table = last_digits.value_counts().sort_index()
prop_table = (last_digits.value_counts(normalize=True).sort_index() * 100).round(2)

df_digits = pd.DataFrame({'Tần số': freq_table, 'Tỉ lệ (%)': prop_table})
print(df_digits)

# 2. Tỉ lệ bội của 5 và 10
m5_count, m5_prop = (h % 5 == 0).sum(), (h % 5 == 0).mean() * 100
m10_count, m10_prop = (h % 10 == 0).sum(), (h % 10 == 0).mean() * 100

print(f"\nBội của 5: {m5_count}/{len(h)} ({m5_prop:.2f}%)")
print(f"Bội của 10: {m10_count}/{len(h)} ({m10_prop:.2f}%)\n")

# 3. So sánh dữ liệu gốc và dữ liệu làm tròn 5 giờ
h_rounded = (h / 5).round() * 5

def get_stats(series):
    return series.mean(), series.median(), series.std(ddof=1), np.percentile(series, 75) - np.percentile(series, 25)

m_orig, med_orig, sd_orig, iqr_orig = get_stats(h)
m_rnd, med_rnd, sd_rnd, iqr_rnd = get_stats(h_rounded)

print("=== BÀI 7: SO SÁNH ĐẠI LƯỢNG TÓM TẮT (GỐC VS LÀM TRÒN 5H) ===")
print(f"Dữ liệu gốc     -> Mean: {m_orig:.2f}, Median: {med_orig:.2f}, SD: {sd_orig:.2f}, IQR: {iqr_orig:.2f}")
print(f"Dữ liệu làm tròn -> Mean: {m_rnd:.2f}, Median: {med_rnd:.2f}, SD: {sd_rnd:.2f}, IQR: {iqr_rnd:.2f}")
