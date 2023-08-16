"""
Created by PerkinsZhu on 2023/8/16 14:43
"""
'''
多行python注释
'''
# 单行python注释

str1 = "hello world" \
       "2323" \
       "end"

print(str1)
print(str1[1:5])
print(str1[-5:-1])
print(str1[-5:])
print(str1[0:3] * 3)
print(str1[-5:-1] + "-=----")

str2='0123456789'
print(str2[0:10])
print(str2[0:10:2])

a = b = c = 1
print(a, b, c)
