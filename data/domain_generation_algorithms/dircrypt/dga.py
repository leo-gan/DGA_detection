import argparse

class RandInt:

    def __init__(self, seed): 
        self.seed = seed

    def rand_int_modulus(self, modulus):
        ix = self.seed                
        ix = 16807*(ix % 127773) - 2836*(ix / 127773) & 0xFFFFFFFF        
        self.seed = ix
        return ix % modulus 

def get_domains(seed, nr):
    r = RandInt(seed)
    for i in range(nr):
        domain_len = r.rand_int_modulus(12+1) + 8
        domain = ""
        for i in range(domain_len):
            char = chr(ord('a') + r.rand_int_modulus(25+1))
            domain += char
        # domain += ".com"
        yield domain

import pandas as pd
if __name__=="__main__":
    # parser = argparse.ArgumentParser(description="generate Dircrypt domains")
    # parser.add_argument("seed", help="seed as hex")
    # args = parser.parse_args()
    # for domain in get_domains(int(args.seed, 16), 30):
    #     print(domain)

    # domains = get_domains(int('0xFFFFFFF1', 16), 30)
    domains = get_domains(12345, 30)
    # for _ in range(100000):
    #     r, domain = generate_domain(charset, r)
    #     domains.append(domain)

    import pandas as pd

    df = pd.DataFrame(data={"domain": domains})
    df = df.drop_duplicates()
    df.to_csv("domains.csv", index=False)
    print(f"Saved {df.shape[0]:,} in domains.csv")
