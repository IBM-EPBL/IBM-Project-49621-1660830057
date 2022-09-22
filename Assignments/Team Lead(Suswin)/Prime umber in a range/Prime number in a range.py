# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 12:16:39 2022

@author: susvin
"""


a = int(input("Enter the lower bound: "))
b = int(input("Enter the upper bound: "))

for i in range(a,b+1):
  if i > 1:
    for j in range(2, i):
      if (i % j) == 0:
        break
    else:
      print(i , " is a prime number")
  else:
      print(i , " is neither prime nor composite")