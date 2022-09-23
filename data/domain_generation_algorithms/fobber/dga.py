import argparse

def ror32(v, n):
    return ((v >> n) | (v << (32-n))) & 0xFFFFFFFF

def next_domain(r, c, l, tld):
    domain = ""
    for _ in range(l):
        r = ror32((321167 * r + c) & 0xFFFFFFFF, 16);
        domain += chr( (r & 0x17FF) % 26 + ord('a') )

    # domain += tld
    # print(domain)
    return r, domain

def dga(version):
    if version == 1:
        r = 0xC87C8A78
        c = -1719405398
        l = 17
        tld = '.net'
        nr = 100000
    elif version == 2:
        r = 0x851A3E59
        c = -1916503263
        l = 10
        tld = '.com'
        nr = 100000
    domains = []

    r = 0xC87C8A78
    c = -1719405398
    l = 17
    tld = '.net'
    nr = 100000
    for _ in range(nr):
        r, domain = next_domain(r, c, l, tld)
        domains.append(domain)

    r = 0x851A3E59
    c = -1916503263
    l = 10
    tld = '.com'
    nr = 100000
    for _ in range(nr):
        r, domain = next_domain(r, c, l, tld)
        domains.append(domain)
    return domains

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="DGA of Fobber")
    parser.add_argument("version", choices=[1,2], type=int)
    args = parser.parse_args()
    domains = dga(args.version)

    # domains = []
    # for _ in range(50000):
    #     domains.append(dga(r))

    import pandas as pd

    df = pd.DataFrame(data={"domain": domains})
    df = df.drop_duplicates()
    df.to_csv("domains.csv", index=False)
    print(f"Saved {df.shape[0]:,} in domains.csv")


