import numpy as np

# 生成一个由 768 个浮点数组成的数组
float_array = np.random.rand(768)

# 将数组转换为逗号分隔的字符串
float_array_str = ', '.join(map(str, float_array))

# 输出逗号分隔的字符串
print(float_array_str)
