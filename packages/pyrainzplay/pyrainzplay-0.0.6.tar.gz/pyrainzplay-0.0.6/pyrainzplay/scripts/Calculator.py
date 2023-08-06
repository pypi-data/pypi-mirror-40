import numpy as np
#from ..funclib.Addition import Addition

def toNumpyArray(a):
    return np.array(a)

if __name__ == '__main__':
    result=toNumpyArray([1,2,3])
    print(result)
    #addResult = Addition.addTwoNumbers(10,10)
    #print("Addition of numbers = "+addResult)


