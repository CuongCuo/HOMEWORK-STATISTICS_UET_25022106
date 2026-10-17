import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== BÀI 10: BỐN KẾT LUẬN, BỐN LOẠI BẪY HỒI QUY ===")

print("""
1. Gọi tên bẫy thống kê chính:
- Trường hợp I (Zagat): Bẫy Ngoại suy (Extrapolation).
- Trường hợp II (Books): Bẫy Diễn giải Sai Hệ số Chặn (Literal Intercept Interpretation / Unrealistic Intercept).
- Trường hợp III (Penguins): Bẫy Simpson / Bỏ qua Biến Nhóm (Simpson's Paradox / Confounding / Aggregation Bias).
- Trường hợp IV (Poverty-Graduates): Bẫy Ngụy biện Sinh thái & Suy diễn Nhân quả (Ecological Fallacy & Causal Inference Error).

2. Viết lại kết luận thành câu thận trọng nhưng vẫn hữu ích:
- I (Zagat): Trong phạm vi điểm số nhà hàng thông thường (food và decor dưới 30), chất lượng món ăn và trang trí có mối liên hệ dương với giá bữa ăn; tuy nhiên không nên dùng mô hình để dự đoán cho các nhà hàng vượt quá thang điểm 30.
- II (Books): Trong phạm vi dữ liệu khảo sát, cuốn sách bìa cứng có cân nặng tăng trung bình 0.72 gram trên mỗi cm³ thể tích, và ở cùng thể tích, sách bìa cứng nặng hơn sách bìa mềm trung bình khoảng 184.05 gram.
- III (Penguins): Xét trong từng loài chim cánh cụt riêng lẻ, mỏ dài hơn đi kèm với mỏ sâu hơn; tuy nhiên sự khác biệt kích thước giữa các loài làm cho xu hướng nhìn gộp bị đảo chiều.
- IV (Poverty-Graduates): Ở cấp độ bang, các bang có tỷ lệ tốt nghiệp trung học cao hơn nhìn chung có tỷ lệ nghèo thấp hơn, nhưng mối liên hệ này bị ảnh hưởng bởi nhiều yếu tố kinh tế - xã hội khác của bang.
""")
