data = [1,2,3,4,5,6,7,8,9,10]

data_mapping = list(map(lambda x: x-1, data))

data_filtering = list(filter(lambda x: x%2 == 0, data_mapping))

from functools import reduce
reduce_data = reduce(lambda x,y: x*y, data_filtering)

print("data_mapping : ", data_mapping)
print("data_filtering : ", data_filtering)
print("reduce_data : ", reduce_data)