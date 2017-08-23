# Local versus global

def local():
    # m doesn't belong to the scope defined by local function
    print(m, 'printing from the local scope')

m = 5

print(m, 'printing from the global scope')

local()
