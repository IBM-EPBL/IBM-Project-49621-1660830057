print("Finding odd numbers in a given range....")

m = int(input("From : "))
n = int(input("To :"))

while m < n+1:
    if(m%2)!=0:
        print("{} is a odd number".format(m))
    m = m + 1
