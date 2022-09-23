import argparse
from ctypes import c_int

class Rand:

    def __init__(self):
        self.r = c_int()

    def srand(self, seed):
        self.r.value = seed

    def rand(self):
        self.r.value = 214013*self.r.value + 2531011
        return (self.r.value >> 16) & 0x7FFF

    def randint(self, lower, upper):
        return lower + self.rand() % (upper - lower + 1)

def dga(r):
    sld = ''.join([chr(r.randint(ord('a'), ord('z'))) for _ in range(10)])
    return sld # + '.com'


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("seed", type=int)
    args = parser.parse_args()
    r = Rand()
    r.srand(args.seed)
    domains = []
    for _ in range(50000):
        domains.append(dga(r))
    
    import pandas as pd

    df = pd.DataFrame(data={"domain": domains})
    df = df.drop_duplicates()
    df.to_csv("domains.csv", index=False)
    print(f"Saved {df.shape[0]:,} in domains.csv")
