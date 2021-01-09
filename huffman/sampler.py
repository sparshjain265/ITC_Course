import random
import numpy as np
import string

l = string.ascii_letters
s = []
for i in l:
	if(i != '\r'):
		s.append(i)
# print(s)
n = len(s)
L = 1024 * 1024

# a = np.random.normal(n/10, n/10, L)
# a = a % n
# with open("sample.txt", 'w+') as f:
# 	for i in a:
# 		f.write(s[int(i)])
	
with open("sample.txt", 'w+') as f:
	f.write(''.join(random.choice(s) for _ in range(L)))