import re
import string

charset = string.hexdigits[0:16]
output = 0
s = "266f479748a0b8772bc328"
for char in s:
    output = output * len(charset) + charset.index(char)
print output