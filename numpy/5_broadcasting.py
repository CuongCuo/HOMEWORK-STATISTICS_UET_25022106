import numpy as np 
# broadcasing ma trận
arr1 = np.array([[1,2,3,4]]) # một ma trận 1 hàng 4 cột
arr2 = np.array([[1],[2],[3],[4]]) # một ma trận 4 hàng 1 cột

print(arr1.shape)
print(arr2.shape)

print(arr1 * arr2)# cả 2 mảng đều scale lên (4,4) 

