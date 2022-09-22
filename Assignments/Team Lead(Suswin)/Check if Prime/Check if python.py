# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 12:00:45 2022

@author: suswin

IBM Assignment - 1 : Check if prime
"""

a = int(input("Enter the number to check if it is a prime : "))

if a > 1:
  for i in range(2, a):
     if (a % i) == 0:
        print(a, " is not a prime number")
        break
  else:
     print(a, " is a prime number")
else:
   print(a, " is neither prime nor composite")