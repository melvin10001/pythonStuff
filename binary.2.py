n = 39
remainders = []
while n > 0:
    n, remainder = divmod(n,2)
    remainders.append(remainder)

# reassing the list to ints reversed copy
remainders = remainders[::-1]
print(remainders)
