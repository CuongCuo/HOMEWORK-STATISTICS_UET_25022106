import sys
import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

print("=== BÀI 1: TÍNH HỆ SỐ TƯƠNG QUAN PEARSON (PENGUINS SAMPLE) ===")

df = pd.DataFrame({
    'chim': [1, 2, 3, 4, 5],
    'x_bill_length': [39.1, 39.5, 40.3, 36.7, 39.3],
    'y_flipper_length': [181, 186, 195, 193, 190]
})

x = df['x_bill_length'].values
y = df['y_flipper_length'].values

x_bar = np.mean(x)
y_bar = np.mean(y)

dx = x - x_bar
dy = y - y_bar
dx_dy = dx * dy
dx2 = dx ** 2
dy2 = dy ** 2

table_df = pd.DataFrame({
    'Chim': df['chim'],
    'x': x,
    'y': y,
    'x - x_bar': dx.round(2),
    'y - y_bar': dy.round(2),
    '(x-x_bar)(y-y_bar)': dx_dy.round(2),
    '(x-x_bar)^2': dx2.round(4),
    '(y-y_bar)^2': dy2.round(2)
})

print("\n1. Trung bình:")
print(f"x_bar = {x_bar:.2f} mm")
print(f"y_bar = {y_bar:.2f} mm")

print("\n2. Bảng tính chi tiết 5 cột:")
print(table_df.to_string(index=False))

sum_dx_dy = np.sum(dx_dy)
sum_dx2 = np.sum(dx2)
sum_dy2 = np.sum(dy2)

print("\n3. Tổng các cột:")
print(f"Sum((x - x_bar)(y - y_bar)) = {sum_dx_dy:.2f}")
print(f"Sum((x - x_bar)^2) = {sum_dx2:.4f}")
print(f"Sum((y - y_bar)^2) = {sum_dy2:.2f}")

r = sum_dx_dy / np.sqrt(sum_dx2 * sum_dy2)
print(f"\nHệ số tương quan Pearson r = {r:.4f}")
