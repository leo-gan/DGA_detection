def map_to_lowercase_letter(s):
    return ord('a') + ((s - ord('a')) % 26)

def get_domains(domain):
    dl = [ord(x) for x in list(domain)]
    dl[0] = map_to_lowercase_letter(dl[0] + dl[3])
    dl[1] = map_to_lowercase_letter(dl[0] + 2*dl[1])
    dl[2] = map_to_lowercase_letter(dl[0] + dl[2] - 1)
    dl[3] = map_to_lowercase_letter(dl[1] + dl[2] + dl[3])
    return ''.join([chr(x) for x in dl])

from random import sample


def get_english_words(data_dir=".", number_words=1, is_long=True, combination_rate=1):
    length = "long" if is_long else "medium"
    file_name = f"{data_dir}/google-10000-english-usa-no-swears-{length}.txt"
    with open(file_name) as f:
        ww = [w.replace('\n', '') for w in sample(f.readlines(), number_words * combination_rate)]
        for i in range(0, number_words * combination_rate, combination_rate):
            yield ''.join(ww[i:i + combination_rate])


# w = get_english_words(data_dir='../../english_words', number_words=3, is_long=True, combination_rate=2)
# print(list(w))


def gen_domain(number_of_seeds, max):
    for seed in get_english_words(data_dir='../../english_words', number_words=number_of_seeds,
                                  is_long=True, combination_rate=3):
        # seed = 'earnestnessbiophysicalohax.com'  # 15372 equal to 0 (seed = 0)
        # print(f"seed: {seed}")
        domain = seed
        for _ in range(max):
            domain = get_domains(domain)
            yield domain


import pandas as pd


def write_file(number_of_seeds, samples_for_seed):
    df = pd.DataFrame(data={"domain": gen_domain(number_of_seeds, samples_for_seed)})
    df = df.drop_duplicates()
    df.to_csv("domains.csv", index=False)
    print(f"Saved {len(df):,} in domains.csv")


number_of_seeds = 500
samples_for_seed = 200
write_file(number_of_seeds, samples_for_seed)
