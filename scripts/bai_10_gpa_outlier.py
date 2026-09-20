import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

sys.stdout.reconfigure(encoding='utf-8')

# --- BÀI 10: Outlier hay lỗi dữ liệu? (gpa_study_hours.csv) ---

# 1. Đọc dữ liệu
study = pd.read_csv("data/gpa_study_hours.csv")
gpa = study["gpa"].dropna()

print(f"Tổng số quan sát ban đầu (N): {len(gpa)}")

# 2. Tìm quan sát GPA > 4
err_obs = gpa[gpa > 4]
print("\n=== BÀI 10: QUAN SÁT VƯỢT NGOÀI MIỀN 0-4 ===")
print(err_obs)

def get_stats(series):
    m = series.mean()
    med = series.median()
    sd = series.std(ddof=1)
    q1, q3 = np.percentile(series, [25, 75])
    iqr = q3 - q1
    return m, med, sd, iqr

# 3. Tính toán trước và sau khi xóa lỗi documented error
m_bef, med_bef, sd_bef, iqr_bef = get_stats(gpa)

gpa_clean = gpa[gpa <= 4]
m_aft, med_aft, sd_aft, iqr_aft = get_stats(gpa_clean)

print("\n=== BÀI 10: ĐẠI LƯỢNG TÓM TẮT TRƯỚC VÀ SAU KHU XÓA LỖI ===")
print(f"Trước khi xóa (N={len(gpa)}):   Mean={m_bef:.4f}, Median={med_bef:.4f}, SD={sd_bef:.4f}, IQR={iqr_bef:.4f}")
print(f"Sau khi xóa   (N={len(gpa_clean)}): Mean={m_aft:.4f}, Median={med_aft:.4f}, SD={sd_aft:.4f}, IQR={iqr_aft:.4f}")

# 4. Tính thay đổi tuyệt đối và tương đối
def calc_changes(bef, aft):
    abs_chg = aft - bef
    rel_chg = (abs_chg / bef) * 100
    return abs_chg, rel_chg

abs_m, rel_m = calc_changes(m_bef, m_aft)
abs_med, rel_med = calc_changes(med_bef, med_aft)
abs_sd, rel_sd = calc_changes(sd_bef, sd_aft)
abs_iqr, rel_iqr = calc_changes(iqr_bef, iqr_aft)

print("\n=== BÀI 10: MỨC ĐỘ THAY ĐỔI (TUYỆT ĐỐI & TƯƠNG ĐỐI %) ===")
print(f"Mean:   Thay đổi tuyệt đối = {abs_m:+.4f}, Tương đối = {rel_m:+.2f}%")
print(f"Median: Thay đổi tuyệt đối = {abs_med:+.4f}, Tương đối = {rel_med:+.2f}%")
print(f"SD:     Thay đổi tuyệt đối = {abs_sd:+.4f}, Tương đối = {rel_sd:+.2f}%")
print(f"IQR:    Thay đổi tuyệt đối = {abs_iqr:+.4f}, Tương đối = {rel_iqr:+.2f}%")

# 5. Vẽ đồ thị so sánh
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.hist(gpa, bins=25, edgecolor='black', color='#C44E52', alpha=0.85)
ax1.set_title(f'GPA trước khi xóa lỗi (N={len(gpa)})\nCó quan sát GPA={err_obs.values[0]} > 4', fontweight='bold')
ax1.set_xlabel('GPA')
ax1.set_ylabel('Frequency')
ax1.grid(axis='y', linestyle='--', alpha=0.5)

ax2.hist(gpa_clean, bins=25, edgecolor='black', color='#4C72B0', alpha=0.85)
ax2.set_title(f'GPA sau khi xóa documented error (N={len(gpa_clean)})\nMiền giá trị hợp lệ [0, 4]', fontweight='bold')
ax2.set_xlabel('GPA')
ax2.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig("output/bai_10_histograms.png", dpi=300)
print("\nĐã lưu biểu đồ: output/bai_10_histograms.png")
