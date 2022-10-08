a = 0 
b = 1
 n = int(input("Enter the range of fibonacci numbers you wish to find"))
print(a) 
print(b)
for i in range(0,n-2):
fib = a + b
print(fib)
a = b
b = fib
i = i + 1
