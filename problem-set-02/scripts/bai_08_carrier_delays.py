import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

# --- BÀI 8: Hãng có nhiều chuyến trễ nhất (nycflights.csv) ---

# 1. Đọc dữ liệu
flights = pd.read_csv("data/nycflights.csv")
f = flights.dropna(subset=["carrier", "arr_delay"]).copy()
f["severe_delay"] = f["arr_delay"] >= 60

# 2. Tổng hợp theo hãng
summary = f.groupby("carrier").agg(
    total_flights=("severe_delay", "count"),
    severe_delay_count=("severe_delay", "sum"),
    severe_delay_rate=("severe_delay", "mean")
).reset_index()

summary["severe_delay_pct"] = (summary["severe_delay_rate"] * 100).round(2)

print("=== BÀI 8: XẾP HẠNG THEO SỐ LƯỢNG CHUYẾN TRỄ (COUNT) ===")
by_count = summary.sort_values(by="severe_delay_count", ascending=False).reset_index(drop=True)
by_count["rank"] = range(1, len(by_count) + 1)
print(by_count[["rank", "carrier", "severe_delay_count", "total_flights"]].to_string(index=False))

print("\n=== BÀI 8: XẾP HẠNG THEO TỈ LỆ CHUYẾN TRỄ (RATE %) ===")
by_rate = summary.sort_values(by="severe_delay_pct", ascending=False).reset_index(drop=True)
by_rate["rank"] = range(1, len(by_rate) + 1)
print(by_rate[["rank", "carrier", "severe_delay_pct", "severe_delay_count", "total_flights"]].to_string(index=False))
