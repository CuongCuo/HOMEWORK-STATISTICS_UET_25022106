import sys
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

print("=== BÀI 9: HAI ĐƯỜNG HỒI QUY KHÔNG PHẢI LÀ HAI CÁCH VIẾT CỦA CÙNG MỘT ĐƯỜNG ===")

r = 0.656
slope_y_on_x = 1.674  # flipper = 127.330 + 1.674 * bill_length

slope_inverse = 1 / slope_y_on_x
print(f"1. Slope của phương trình giải ngược = 1 / {slope_y_on_x} = {slope_inverse:.4f}")

# Slope OLS thực tế của x trên y: b_{x|y} = r^2 * (1 / b_{y|x})
slope_x_on_y_ols = (r ** 2) * slope_inverse
print(f"2. Slope OLS thực tế của bill_length trên flipper_length = r^2 * (1 / b_{{y|x}}) = {r:.3f}^2 * {slope_inverse:.4f} = {slope_x_on_y_ols:.4f}")

print(f"\n3. Chênh lệch giữa hai đường: Slope OLS thực tế ({slope_x_on_y_ols:.4f}) khác biệt đáng kể so với Slope giải ngược ({slope_inverse:.4f}).")
print("Nguyên nhân: Hồi quy y theo x tối thiểu hóa sai số chiều dọc, còn hồi quy x theo y tối thiểu hóa sai số chiều ngang.")
