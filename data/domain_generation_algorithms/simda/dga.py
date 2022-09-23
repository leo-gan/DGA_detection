length = 7
tld = "com"
key = "1676d5775e05c50b46baa5579d4fc7"
base = 0x45AE94B2

consonants = "qwrtpsdfghjklzxcvbnmv"
vowels = "eyuioa"

step = 0
for m in key:
    step += ord(m)

domains = []
from random import randint
for nr in range(200000):
    domain = ""
    base += step

    for i in range(randint(7, 18)):
        index = int(base/(3+2*i))
        if i % 2 == 0:
            char = consonants[index % 20]
        else:
            char = vowels[index % 6]
        domain += char
    domains.append(domain)
    # domain += "." + tld
    # print(domain)

    # domains = get_domains(123, 100000, tlds)
    # for sequence_nr in range(100000):
    #     domains.append(generate_necurs_domain(sequence_nr, 9, date))

import pandas as pd

df = pd.DataFrame(data={"domain": domains})
print(f"Created df: {df.shape[0]:,}")
df = df[df['domain'].str.len() > 6]
df = df.drop_duplicates()
df.to_csv("domains.csv", index=False)
print(f"Saved {df.shape[0]:,} in domains.csv")
