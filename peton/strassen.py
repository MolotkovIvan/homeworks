import math
import numpy as np


def read_array(n):
    size = 2**(math.ceil(math.log2(n)))
    a = np.array([[float(i) for i in input().split()] for j in range(n)])
    return np.vstack((np.hstack((a, np.zeros((n, size-n)))),
                     np.zeros((size-n, size))))


def write_array(arr):
    for i in arr:
        print(' '.join([str(int(j)) for j in i]))


def quartering(m):
    size = len(m)//2
    m11 = m[0:size, 0:size]
    m12 = m[0:size, size:size*2]
    m21 = m[size:size*2, 0:size]
    m22 = m[size:size*2, size:size*2]
    return m11, m12, m21, m22


def strassen(a, b):
    if len(a) == 1:
        return a*b

    a11, a12, a21, a22 = quartering(a)
    b11, b12, b21, b22 = quartering(b)
    p1 = strassen(a11 + a22, b11 + b22)
    p2 = strassen(a21 + a22, b11)
    p3 = strassen(a11, b12 - b22)
    p4 = strassen(a22, b21 - b11)
    p5 = strassen(a11 + a12, b22)
    p6 = strassen(a21 - a11, b11 + b12)
    p7 = strassen(a12 - a22, b21 + b22)

    c11 = p1 + p4 - p5 + p7
    c12 = p3 + p5
    c21 = p2 + p4
    c22 = p1 - p2 + p3 + p6

    c = np.vstack((np.hstack((c11, c12)), np.hstack((c21, c22))))
    return c

if __name__ == "__main__":
    n = int(input())
    a = read_array(n)
    b = read_array(n)
    c = strassen(a, b)
    c = c[0:n, 0:n]
    write_array(c)
