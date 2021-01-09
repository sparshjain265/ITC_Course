import nhuffman as hc

n = int(input("Enter n: "))
h = hc.huffmanCoding(n)
h.compress()
h.decompress()
