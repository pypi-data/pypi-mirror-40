import numpy as np
import cos_doubles

x = np.arange(0, 2 * np.pi, 0.1)

#x = np.array([[1,2,3],[4,5,6]],dtype=float32)
y = np.empty_like(x)

cos_doubles.cos_doubles_func(x, y)

print(x)
print(y)
