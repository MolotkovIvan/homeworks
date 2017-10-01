import math
import numpy as np


def read_matrix(n):
    return np.array([list(map(int, input().split())) for _ in range(n)])


def write_matrix(m):
    for row in m:
        print(' '.join(map(str, row)))


def strassen(a, b):
    if a.shape == (1, 1):
        return a * b

    av = np.vsplit(a, 2)
    a11, a12 = np.hsplit(av[0], 2)
    a21, a22 = np.hsplit(av[1], 2)

    bv = np.vsplit(b, 2)
    b11, b12 = np.hsplit(bv[0], 2)
    b21, b22 = np.hsplit(bv[1], 2)

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
    a = np.zeros((size, size), int)
    a[0:n, 0:n] = read_matrix(n)
    b = np.zeros((size, size), int)
    b[0:n, 0:n] = read_matrix(n)
    c = strassen(a, b)
    write_matrix(c[0:n, 0:n])
