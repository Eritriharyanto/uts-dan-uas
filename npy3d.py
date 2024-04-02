import numpy as np

data = np.array([[[4, 1], [5, 2], [3, 8]],
				 [[2, 4], [7, 9], [5, 9]],
				 [[9, 4], [2, 3], [4, 1]]])

data_1 = data[2][1][0]
data_2 = data[1][1][1]
data_3 = data[0][2][1]


print("Data[2][1][0]:", data_1)
print("Data[1][1][1]:", data_2)
print("Data[0][2][1]:", data_3)