import numpy as np

ages = np.array([[22,25,18,35,45,29],
                [30,40,25,35,45,20]])

teen = ages[ages < 20] # có thể lọc bằng & và | để lọc nhiều điều kiện

adults = np.where(ages >= 18, ages, 'teen') # có thể dùng np.where để lọc điều kiện

print(teen) # trả về ma trận 
print(adults)  
