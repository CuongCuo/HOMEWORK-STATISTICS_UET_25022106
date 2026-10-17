import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== BÀI 6: TỰ CHẠY MÔ HÌNH STAT20 PENGUINS TRÊN GIẤY ===")

# M2: flipper_hat = 147.563 + 1.096 * bill_length - 5.247 * I(Chinstrap) + 17.552 * I(Gentoo)
# Tham chiếu là Adelie

bill_length = 43

pred_adelie = 147.563 + 1.096 * bill_length
pred_chinstrap = 147.563 + 1.096 * bill_length - 5.247
pred_gentoo = 147.563 + 1.096 * bill_length + 17.552

print(f"1. Với bill_length = {bill_length} mm, dự đoán của M2:")
print(f"Adelie:    {pred_adelie:.3f} mm")
print(f"Chinstrap: {pred_chinstrap:.3f} mm")
print(f"Gentoo:    {pred_gentoo:.3f} mm")

# Đổi tham chiếu sang Chinstrap:
# b0_new = 147.563 - 5.247 = 142.316
# I(Adelie) = +5.247
# I(Gentoo) = 17.552 - (-5.247) = 22.799

b0_new = 147.563 - 5.247
b_adelie = 5.247
b_gentoo = 17.552 + 5.247

print(f"\n2. Phương trình M2 với Chinstrap là tham chiếu:")
print(f"flipper_hat = {b0_new:.3f} + 1.096 * bill_length + {b_adelie:.3f} * I(Adelie) + {b_gentoo:.3f} * I(Gentoo)")

pred_gentoo_new = b0_new + 1.096 * bill_length + b_gentoo
print(f"\n3. Kiểm tra lại dự đoán cho Gentoo mỏ 43 mm bằng phương trình mới:")
print(f"Dự đoán Gentoo mới: {pred_gentoo_new:.3f} mm (Trùng khớp 100%)")
