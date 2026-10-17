import numpy as np 

arr = np.array([[1,2,3,4],
                [5,6,7,8],
                [9,10,11,12],
                [13,14,15,16]])
#arr[start:end:step]
print(arr[0]) # [1 2 3 4]
print(arr[0:4:2]) # [1,2,3,4] \n [9,10,11,12]
