import math
import numpy as np


def read_array(n):
    return np.array([list(map(int, input().split())) for _ in range(n)])


def write_array(arr, n):
    arr = arr[0:n, 0:n]
    for i in arr:
        print(' '.join(map(str, i)))


def split(m):
    size = len(m)
    m11 = m[0:size // 2, 0:size // 2]
    m12 = m[0:size // 2, size // 2:size]
    m21 = m[size // 2:size, 0:size // 2]
    m22 = m[size // 2:size, size // 2:size]
    return m11, m12, m21, m22


def strassen(a, b):
    if a.shape == (1, 1):
        return a * b

    a11, a12, a21, a22 = split(a)
    b11, b12, b21, b22 = split(b)
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

    return np.vstack((np.hstack((c11, c12)),
                      np.hstack((c21, c22))))

if __name__ == "__main__":
    n = int(input())
    size = 2 ** (math.ceil(math.log2(n)))
    a = np.vstack((np.hstack((read_array(n), np.zeros((n, size - n), int))),
                   np.zeros((size - n, size), int)))
    b = np.vstack((np.hstack((read_array(n), np.zeros((n, size - n), int))),
                   np.zeros((size - n, size), int)))
    c = strassen(a, b)
    write_array(c, n)
