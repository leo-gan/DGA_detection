from random import sample


def get_word(data_dir=".", is_long=True):
    length = "long" if is_long else "medium"
    file_name = f"{data_dir}/google-10000-english-usa-no-swears-{length}.txt"
    with open(file_name) as f:
        return sample(f.readlines(), 1)[0].replace('\n', '')


def get_english_words(data_dir=".", number_words=1, is_long=True):
    length = "long" if is_long else "medium"
    file_name = f"{data_dir}/google-10000-english-usa-no-swears-{length}.txt"
    with open(file_name) as f:
        return [w.replace('\n', '') for w in sample(f.readlines(), number_words)]

w = get_word(is_long=False)
print(w)
