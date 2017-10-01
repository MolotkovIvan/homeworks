import math
import numpy as np


def strassen(a, b):
	if len(a) == 1:
		return a*b
	
	size = len(a)//2

	a11 = a[0:size, 0:size]
	a12 = a[0:size, size:size*2]
	a21 = a[size:size*2, 0:size]
	a22 = a[size:size*2, size:size*2]

	b11 = b[0:size, 0:size]
	b12 = b[0:size, size:size*2]
	b21 = b[size:size*2, 0:size]
	b22 = b[size:size*2, size:size*2]

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
	c = np.vstack((np.hstack((c11,c12)), np.hstack((c21, c22))))
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
c = c[0:n, 0:n]
for i in range(len(c)):
	print(' '.join([str(int(j)) for j in c[i]]))