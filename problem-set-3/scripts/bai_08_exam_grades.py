import sys
from pathlib import Path
import pandas as pd
import numpy as np
from plotnine import (
    ggplot, aes, geom_histogram, facet_wrap, labs, theme_minimal
)

sys.stdout.reconfigure(encoding='utf-8')

data_path = Path("data/exam_grades.csv")
if not data_path.exists():
    data_path = Path("../data/exam_grades.csv")

df = pd.read_csv(data_path)

print("=== BÀI 8: PHÂN TÍCH ĐIỂM SỐ KHÓA HỌC (EXAM GRADES) ===")
clean_df = df.dropna(subset=['course_grade']).copy()
print(f"Tổng số sinh viên: {len(clean_df)}")

# Thống kê điểm course_grade
cg = clean_df['course_grade']
print(f"Course grade - Min: {cg.min()}, Max: {cg.max()}, Mean: {cg.mean():.2f}, Median: {cg.median():.2f}")

# Kiểm tra các điểm tụ xung quanh các mốc Pass (ví dụ 60, 70, 75, 80, 90)
print("\nPhân bố điểm course_grade nguyên gần mốc đậu/đổi điểm (ví dụ 69-71, 74-76, 79-81, 89-91):")
print(cg.value_counts().sort_index().tail(25))

# Đồ thị 1: Bin width 5 vs Bin width 1
p1 = (
    ggplot(clean_df, aes(x='course_grade'))
    + geom_histogram(binwidth=5, color='white', fill='#4C72B0')
    + labs(
        title="Hình 8A: Course Grade với Bin Width = 5",
        x="Course Grade",
        y="Số lượng sinh viên"
    )
    + theme_minimal()
)

p2 = (
    ggplot(clean_df, aes(x='course_grade'))
    + geom_histogram(binwidth=1, color='white', fill='#C44E52')
    + labs(
        title="Hình 8B: Course Grade với Bin Width = 1 (Tụ điểm chi tiết)",
        x="Course Grade",
        y="Số lượng sinh viên"
    )
    + theme_minimal()
)

p3 = (
    ggplot(clean_df, aes(x='course_grade'))
    + geom_histogram(binwidth=2, color='white', fill='#55A868')
    + facet_wrap('~ semester', labeller=lambda s: f"Học kỳ: {s}")
    + labs(
        title="Hình 8C: Phân bố Course Grade theo Học kỳ (Semester)",
        x="Course Grade",
        y="Số lượng sinh viên"
    )
    + theme_minimal()
)

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)
p2.save("output/bai_08_histograms.png", width=8, height=4, dpi=300)
p3.save("output/bai_08_by_semester.png", width=8, height=5, dpi=300)
print("\nĐã lưu biểu đồ thành công: output/bai_08_histograms.png và output/bai_08_by_semester.png")
