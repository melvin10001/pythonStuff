order_total = 247 #GBP

if order_total > 100:
    discount = 25
else:
    discount = 0
print(order_total, discount)

discount = 25 if order_total > 100 else 0

print(order_total, discount)
