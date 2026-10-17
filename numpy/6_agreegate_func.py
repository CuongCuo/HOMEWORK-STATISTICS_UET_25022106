import numpy as np 
# hàm này tổng hợp các giá trị lại và trả về 1 giá trị uy nhất
arr = ([[1,2,3,4,5],
        [6,7,8,9,10]])

print(np.sum(arr)) # tổng tất cả các phần tử trong mảng

print(np.mean(arr)) # trung bình tất cả các phần tử trong mảng
print(np.std(arr)) # độ lệch chuẩn tất cả các phần tử trong mảng
print(np.var(arr)) # phương sai tất cả các phần tử trong mảng

print(np.min(arr)) # giá trị nhỏ nhất tất cả các phần tử trong mảng
print(np.argmin(arr)) # trả về index min 
print(np.max(arr)) # giá trị lớn nhất tất cả các phần tử trong mảng

print(np.median(arr)) # trung vị tất cả các phần tử trong mảng
