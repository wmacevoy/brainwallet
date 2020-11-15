# ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
# ALPHABET = "ABDEFGHNQRTabdefghnqrt"
# ALPHABET = "ABDEFHJNQRT39"

# ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def encode(num):
    acc = num
    enc = ""
    while True:
        acc, idx = divmod(acc, len(ALPHABET))
        digit = ALPHABET[idx: idx + 1]
        enc = str(digit) + str(enc)
        if acc == 0: break
    return enc

def decode(enc):
    acc = 0
    for k in range(len(enc)):
        digit = enc[k:k+1]
        idx = ALPHABET.index(digit)
        acc=len(ALPHABET)*acc+idx
    num = acc
    return num

def test():
    for num in range(len(ALPHABET)**3):
        enc = encode(num)
        dec = decode(enc)
        assert len(enc) > 0
        assert num == dec

test()
for num in range(2048):
    print (encode(num))
