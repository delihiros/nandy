def nth(data, n): # index from bottom
    return (data >> n) & 1

# def extract(data, s, e): # index from bottom
#     out = 0
#     for bit in reversed([nth(data, i) for i in range(s, e)]):
#         out = (out << 1) | bit
#     return out

def extract(data, s, e, bit=16):
    form = '{:0' + str(bit) + 'b}'
    bin_str = form.format(data, 2)
    rbin_str = bin_str[::-1]
    rbits = rbin_str[s:e]
    bits = int(rbits[::-1], 2)
    return bits

# a = 0b100111
# print(bin(a))
# print([nth(a, i) for i in range(6)])
# print(bin(extract(a, 3, 7)))
