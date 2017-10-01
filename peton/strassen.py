import math
import numpy as np


def strassen(a, b):
	if len(a) == 1:
		return a*b
	
	size = len(a)//2

	a11 = np.zeros((size, size))
	a12 = np.zeros((size, size))
	a21 = np.zeros((size, size))
	a22 = np.zeros((size, size))

	b11 = np.zeros((size, size))
	b12 = np.zeros((size, size))
	b21 = np.zeros((size, size))
	b22 = np.zeros((size, size))

	for i in range(size):
		for j in range(size):
			a11[i][j] = a[i][j]
			a12[i][j] = a[i][j+size]
			a21[i][j] = a[i+size][j]
			a22[i][j] = a[i+size][j+size]

			b11[i][j] = b[i][j]
			b12[i][j] = b[i][j+size]
			b21[i][j] = b[i+size][j]
			b22[i][j] = b[i+size][j+size]
	
	p1 = strassen(a11 + a22, b11 + b22)#(a11 + a22)(b11+b22)
	p2 = strassen(a21 + a22, b11)#(a21 + a22)(b11)
	p3 = strassen(a11, b12 - b22)#a11(b12-b22)
	p4 = strassen(a22, b21 - b11)#a22(b21-b11)
	p5 = strassen(a11 + a12, b22)#(a11+a12)b22
	p6 = strassen(a21 - a11, b11 + b12)#(a21-a11)(b11+b12)
	p7 = strassen(a12 - a22, b21 + b22)#(a12-a22)(b21+b22)

	c11 = p1 + p4 - p5 + p7 #p1 + p4 - p5 + p7
	c12 = p3 + p5 #p3 + p5
	c21 = p2 + p4 #p2 + p4
	c22 = p1 - p2 + p3 + p6#p1 - p2 + p3 + p6
	c = np.zeros((size*2, size*2))
	for i in range(size):
		for j in range(size):
			c[i][j] = c11[i][j]
			c[i][j+size] = c12[i][j]
			c[i+size][j] = c21[i][j]
			c[i+size][j+size] = c22[i][j]
	return(c)




n = int(input())
size = 2**(math.ceil(math.log2(n)))

a = np.zeros((size, size))
b = np.zeros((size, size))

for i in range(n):
	q = input().split()
	for j in range(n):
		a[i][j] = int(q[j]);

for i in range(n):
	q = input().split()
	for j in range(n):
		b[i][j] = int(q[j]);

c = strassen(a, b)
for i in range(n):
	for j in range(n):
		print(int(c[i][j]), end=" ")
	print()