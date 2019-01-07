def nth(data, n): # index from bottom
    return (data >> n) & 1

def extract(data, s, e): # index from bottom
    out = 0
    for bit in reversed([nth(data, i) for i in range(s, e)]):
        out = (out << 1) | bit
    return out

# a = 0b100111
# print(bin(a))
# print([nth(a, i) for i in range(6)])
# print(bin(extract(a, 3, 7)))
