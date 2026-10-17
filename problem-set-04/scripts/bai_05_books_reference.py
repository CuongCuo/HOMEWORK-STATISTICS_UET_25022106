import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== BÀI 5: ĐỔI MỨC THAM CHIẾU MÀ KHÔNG KHỚP LẠI MÔ HÌNH ===")

# Mô hình gốc (hb là tham chiếu): weight_hat = 197.96 + 0.72 * volume - 184.05 * I(pb)
# Đổi mức tham chiếu sang pb: H = 1 nếu hb, H = 0 nếu pb => I(pb) = 1 - H
# weight_hat = 197.96 + 0.72 * volume - 184.05 * (1 - H)
# weight_hat = (197.96 - 184.05) + 0.72 * volume + 184.05 * H
# weight_hat = 13.91 + 0.72 * volume + 184.05 * H

a0 = 197.96 - 184.05
a1 = 0.72
a2 = 184.05

print(f"1. Phương trình mới với pb là tham chiếu:")
print(f"weight_hat = {a0:.2f} + {a1:.2f} * volume + {a2:.2f} * H")

volume_val = 900

# Cách gốc:
pred_hb_orig = 197.96 + 0.72 * volume_val - 184.05 * 0
pred_pb_orig = 197.96 + 0.72 * volume_val - 184.05 * 1

# Cách mới:
pred_hb_new = a0 + a1 * volume_val + a2 * 1
pred_pb_new = a0 + a1 * volume_val + a2 * 0

print(f"\n2. Kiểm tra với volume = {volume_val}:")
print(f"Bìa cứng (hb) - Gốc: {pred_hb_orig:.2f}g, Mới: {pred_hb_new:.2f}g (Trùng khớp)")
print(f"Bìa mềm (pb)  - Gốc: {pred_pb_orig:.2f}g, Mới: {pred_pb_new:.2f}g (Trùng khớp)")

print("\n3. Đại lượng không đổi: Khoảng cách dự đoán giữa hai loại bìa (|184.05g|).")
