phrase = "Don't panic!"
plist = list(phrase)
print(phrase)
print(plist)

plist = plist[1:8]
first = plist[0:2]
second = plist[3:7]
first.extend(second[1])
first.extend(second[0])
first.extend(second[2:])
print(''.join(first[0:4]) + ''.join(first[-1:-3:-1]))
