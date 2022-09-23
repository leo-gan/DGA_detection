import glob
import pandas as pd


def add_tdl(df, domain_field):
    if not df.empty and "." not in str(df.loc[0, domain_field]):
        df[domain_field] = df[domain_field].apply(lambda d: f'{d}.com')
    return df


def get_df(file, field, domain_field):
    df = pd.read_csv(file, nrows=None, usecols=[field]).rename(columns={field: domain_field}).dropna()
    df = add_tdl(df, domain_field=domain_field)
    print(f"  Loaded {file}, {df.shape[0]:,}. Example: {df.loc[0, domain_field]}")
    return df


def get_all_domains(dir2field):
    domain_field = 'domain'
    dfs = []
    for subdir, field in dir2field.items():
        # get files is subdir:
        print(f" {subdir}:")
        pattern = f"{subdir}/*.csv"
        df = pd.concat([get_df(f, field=field, domain_field=domain_field) for f in glob.glob(pattern)])
        print(f"    Concatenated: {df.shape[0]:,}")
        df = df.drop_duplicates()
        print(f"    Deduplicated: {df.shape[0]:,}")
        dfs.append(df)

    df = pd.concat(dfs)
    print(f"Concatenated {df.shape[0]:,}")
    df = df.drop_duplicates()
    print(f"    Deduplicated: {df.shape[0]:,}")

    output_file = f"Adversarial-DGA-Datasets.{df.shape[0] // 1_000}K.csv"
    df.to_csv(output_file, index=False)
    print(f"Saved  {df.shape[0]:,} into {output_file}")


dir2field = {
    "AppendAttack": "url_original",
    "RandomAttack": "url_original",
    "SearchAttack": "url_original",
    "MaskDGA": "url_original",
    "CharBot": "url",
    "DeepDGA": "domain",
}
get_all_domains(dir2field)