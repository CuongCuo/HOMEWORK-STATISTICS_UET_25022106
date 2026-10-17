import numpy as np 

arr = np.array([[['A','B','C'],['A','B','C'],['A','B','_']],
               [['A','B','C'],['A','B','C'],['A','B','_']],
               [['A','B','C'],['A','B','C'],['A','B','_']]])

print(arr.ndim) # in ra số chiều
print(arr.shape) # in ra hình dáng : layer -> row -> columm

word = arr[0,0,0] + arr[2,0,0]
print(word)