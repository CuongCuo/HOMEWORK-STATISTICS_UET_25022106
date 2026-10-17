import pandas as pd
#Series = mảng 1 chiều , (có idx và value) (ma trận 1 cột n hàng)

data = [100,102,104]

series = pd.Series(data, index = ['a','b','c']) #index đổi tên số thứ tự 
print(series)
