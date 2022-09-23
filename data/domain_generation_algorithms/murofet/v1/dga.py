import hashlib
from datetime import datetime, timedelta
import argparse


def dga(date):

    for index in range(1020):
        seed = 7*[0]
        seed[0] = ((date.year & 0xFF) + 0x30) & 0xFF
        seed[1] = date.month 
        seed[2] = (date.day//7)*7
        r = index
        for i in range(4):
            seed[3+i] = r & 0xFF
            r >>= 8

        seed_str = ""
        for i in range(7):
            seed_str += chr((seed[i]))

        m = hashlib.md5()
        m.update(seed_str)
        md5 = m.digest()

        domain = ""
        for m in md5:
            d = (ord(m) & 0x1F) + ord('a')
            c = (ord(m) >> 3) + ord('a')
            if d != c:
                if d <= ord('z'):
                    domain += chr(d)
                if c <= ord('z'):
                    domain += chr(c)
            yield domain

        # tlds = [".ru", ".biz", ".info", ".org", ".net", ".com"]
        # for i, tld in enumerate(tlds):
        #     m = len(tlds) - i
        #     if not index % m:
        #         domain += tld
        #         break
        # # print(domain)
        # yield domain

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="date for which to generate domains")
    args = parser.parse_args()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()
    # dga(d)
    domains = dga(d)

    import pandas as pd

    df = pd.DataFrame(data={"domain": domains})
    print(f"Created df: {df.shape[0]:,}")
    df = df.drop_duplicates()
    df.to_csv("domains.csv", index=False)
    print(f"Saved {df.shape[0]:,} in domains.csv")
