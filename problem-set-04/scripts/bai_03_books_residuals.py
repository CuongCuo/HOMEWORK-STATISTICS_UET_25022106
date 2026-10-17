import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

print("=== BÀI 3: RESIDUAL ACCOUNTING (BOOKS DATASET) ===")

df = pd.DataFrame({
    'id': [4, 8, 11, 13],
    'volume': [239, 412, 1492, 1010],
    'weight': [350, 250, 975, 950],
    'cover': ['hb', 'pb', 'pb', 'pb']
})
df['I_pb'] = (df['cover'] == 'pb').astype(int)

# Model 0: weight_hat = 108 + 0.71 * volume
df['yhat0'] = 108 + 0.71 * df['volume']
df['e0'] = df['weight'] - df['yhat0']
df['e0_sq'] = df['e0'] ** 2

# Model 1: weight_hat = 197.96 + 0.72 * volume - 184.05 * I_pb
df['yhat1'] = 197.96 + 0.72 * df['volume'] - 184.05 * df['I_pb']
df['e1'] = df['weight'] - df['yhat1']
df['e1_sq'] = df['e1'] ** 2

print("\n1. Kết quả Mô hình M0 (chỉ dùng volume):")
print(df[['id', 'volume', 'weight', 'yhat0', 'e0', 'e0_sq']].round(2).to_string(index=False))
sse0 = df['e0_sq'].sum()
print(f"SSE0 trên 4 cuốn này = {sse0:.2f}")

print("\n2. Kết quả Mô hình M1 (dùng volume + cover):")
print(df[['id', 'volume', 'weight', 'yhat1', 'e1', 'e1_sq']].round(2).to_string(index=False))
sse1 = df['e1_sq'].sum()
print(f"SSE1 trên 4 cuốn này = {sse1:.2f}")

print(f"\n3. So sánh SSE: SSE1 ({sse1:.2f}) < SSE0 ({sse0:.2f}) => Mô hình M1 thắng trên tập 4 cuốn này.")
print("Cuốn sách có e^2 lớn hơn ở M1 là ID 13 (tăng từ 15600.01 lên 43635.03).")
