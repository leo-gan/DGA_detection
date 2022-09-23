from random import randint
def dga(seed, nr):
    s = (2 * seed * (nr + 1))
    r = s ^ (26 * seed * nr)
    domain = ""
    for i in range(randint(12, 18)):
        r = r & 0xFFFFFFFF
        domain += chr(r % 26 + ord('a'))
        r += (r ^ (s*i**2*26))
 
    # domain += ".org"
    yield domain

domains = []
for nr in range(200000):
    domains += list(dga(0xD5FFF, nr))


# domains = [dga(0xD5FFF, nr) for nr in range(100)]
# for sequence_nr in range(100000):
#     domains.append(generate_necurs_domain(sequence_nr, 9, date))

import pandas as pd

df = pd.DataFrame(data={"domain": domains})
print(f"Created df: {df.shape[0]:,}")
# df = df[df['domain'].str.len() > 6]
df = df.drop_duplicates()
df.to_csv("domains.csv", index=False)
print(f"Saved {df.shape[0]:,} in domains.csv")
