import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding='utf-8')

print("=== BÀI 2: ĐƯỜNG HỒI QUY BÌNH PHƯƠNG TỐI THIỂU (ZAGAT 4 NHÀ HÀNG) ===")

df = pd.DataFrame({
    'nha_hang': ["Daniella Ristorante", "Tello's Ristorante", "Pasticcio", "Belluno"],
    'food': [22, 20, 20, 22],
    'price': [43, 32, 34, 39]
})

x = df['food'].values
y = df['price'].values

x_bar = np.mean(x)
y_bar = np.mean(y)

dx = x - x_bar
dy = y - y_bar

b1 = np.sum(dx * dy) / np.sum(dx ** 2)
b0 = y_bar - b1 * x_bar

y_hat = b0 + b1 * x
e = y - y_hat
sse = np.sum(e ** 2)

print(f"x_bar (food) = {x_bar:.2f}")
print(f"y_bar (price) = {y_bar:.2f}")
print(f"Hệ số góc b1 = {b1:.2f}")
print(f"Hệ số chặn b0 = {b0:.2f}")
print(f"Phương trình OLS: price_hat = {b0:.2f} + {b1:.2f} * food")

res_df = pd.DataFrame({
    'Nhà hàng': df['nha_hang'],
    'food (x)': x,
    'price (y)': y,
    'price_hat (y_hat)': y_hat,
    'Residual (e)': e,
    'e^2': e ** 2
})
print("\nBảng dự đoán và phần dư:")
print(res_df.to_string(index=False))

print(f"\nKiem tra Sum(e) = {np.sum(e):.2f}")
print(f"Kiem tra Sum(x * e) = {np.sum(x * e):.2f}")
print(f"SSE = Sum(e^2) = {sse:.2f}")

# Đoạn mã đổi thang điểm 0-100: x* = (100/30) x => x = (3/10) x*
b1_star = b1 * 0.3
print(f"\nKhi đổi thang điểm 0-100: price_hat = {b0:.2f} + {b1_star:.2f} * x*")
print("Hệ số Pearson r giữ nguyên không đổi.")

plt.figure(figsize=(6, 4))
plt.scatter(x, y, color='blue', s=80, label='Dữ liệu thực tế')
plt.plot(x, y_hat, color='red', linestyle='--', label=f'OLS: y = {b0:.1f} + {b1:.1f}x')
plt.title('Hồi quy OLS Giá ăn theo Chất lượng món (Zagat)')
plt.xlabel('Food rating (0-30)')
plt.ylabel('Price ($)')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.savefig('output/bai_02_ols.png', dpi=300)
print("Đã lưu biểu đồ: output/bai_02_ols.png")
