from ctypes import c_uint
import argparse

class Rand():

    def __init__(self, seed):
        self.r = c_uint(seed)
        self.m = 1103515245
        self.a = 12345

    def rand(self):
        self.r.value = self.r.value*self.m + self.a
        self.r.value &= 0x7FFFFFFF
        return self.r.value


def dga(r):
    length = r.rand()%14 + 7
    domain = ""
    for i in range(length):
        domain += chr(r.rand() % 26 + ord('a'))
    # domain += ".top"
    # print(domain)
    return domain

if __name__=="__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("seed", help="e.g. DEADBEEF")
    # args = parser.parse_args()
    r = Rand(123456)
    domains = []
    for nr in range(200000):
        domains.append(dga(r))

    # domains = dga(args.seed, d)

    import pandas as pd

    df = pd.DataFrame(data={"domain": domains})
    print(f"Created df: {df.shape[0]:,}")
    df = df[df['domain'].str.len() > 6]
    df = df.drop_duplicates()
    df.to_csv("domains.csv", index=False)
    print(f"Saved {df.shape[0]:,} in domains.csv")
