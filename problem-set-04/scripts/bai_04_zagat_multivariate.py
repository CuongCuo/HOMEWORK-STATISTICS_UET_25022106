import sys
import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

print("=== BÀI 4: HỒI QUY NHIỀU BIẾN BẰNG PHƯƠNG TRÌNH CHUẨN (ZAGAT) ===")

x = np.array([22, 20, 20, 22])
y = np.array([43, 32, 34, 39])
W = np.array([1, 1, 0, 0])

n = len(x)
sum_x = np.sum(x)
sum_W = np.sum(W)
sum_y = np.sum(y)

sum_x2 = np.sum(x ** 2)
sum_xW = np.sum(x * W)
sum_W2 = np.sum(W ** 2)

sum_xy = np.sum(x * y)
sum_Wy = np.sum(W * y)

print("Hệ 3 phương trình chuẩn:")
print(f"1) {n}*b0 + {sum_x}*b1 + {sum_W}*b2 = {sum_y}")
print(f"2) {sum_x}*b0 + {sum_x2}*b1 + {sum_xW}*b2 = {sum_xy}")
print(f"3) {sum_W}*b0 + {sum_xW}*b1 + {sum_W2}*b2 = {sum_Wy}")

A = np.array([
    [n, sum_x, sum_W],
    [sum_x, sum_x2, sum_xW],
    [sum_W, sum_xW, sum_W2]
], dtype=float)

B = np.array([sum_y, sum_xy, sum_Wy], dtype=float)

b = np.linalg.solve(A, B)
b0, b1, b2 = b

print(f"\nNghiệm: b0 = {b0:.2f}, b1 = {b1:.2f}, b2 = {b2:.2f}")
print(f"Phương trình OLS: y_hat = {b0:.2f} + {b1:.2f}*x + {b2:.2f}*W")

y_hat = b0 + b1 * x + b2 * W
e = y - y_hat
sse = np.sum(e ** 2)

res_df = pd.DataFrame({
    'x (food)': x,
    'y (price)': y,
    'W (west)': W,
    'y_hat': y_hat,
    'e': e,
    'e^2': e ** 2
})

print("\nBảng phần dư:")
print(res_df.to_string(index=False))
print(f"\nSSE (mô hình 2 biến) = {sse:.2f} (so với SSE bài 2 = 10.00)")
