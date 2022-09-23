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


def get_all_domains(out_file, nrows):
    domain_field = 'domain'
    dfs = []
    # for subdir, field in dir2field.items():
        # get files is subdir:
        # print(f" {subdir}:")
    pattern = f"*/domains.csv"
    # print(glob.glob(pattern))
    df = pd.DataFrame()
    i = 0
    for f in glob.glob(pattern):
        df_ind = pd.read_csv(f, nrows=nrows)
        print(f"    Loaded {df_ind.shape[0]:,}, {f}")
        df_ind["domain"] = df_ind["domain"].apply(lambda d: d.split('.')[0])
        df = pd.concat([df, df_ind])
        print(f"    Concatenated: {df_ind.shape[0]:,} -> {df.shape[0]:,}")
        df = df.drop_duplicates()
        print(f"      Deduplicated: {df.shape[0]:,}")
        i += 1

    output_file = f"{out_file[:-4]}.{i+1}_algos.{df.shape[0] // 1_000_000}M.csv"
    df.to_csv(output_file, index=False)
    print(f"Saved  {df.shape[0]:,} into {output_file}")


nrows = 200000
out_file = "malignant_domains.dga_generated.csv"
get_all_domains(out_file, nrows=nrows)
