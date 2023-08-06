import numpy as np

def toNumpyArray(a):
    return np.array(a)

if __name__ == '__main__':
    result=toNumpyArray([1,2,3])
    print(result)
