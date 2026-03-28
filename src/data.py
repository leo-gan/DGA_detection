import glob
import pandas as pd
import tldextract
from sklearn.utils import shuffle


def read_data(file_name):
    with open(file_name, encoding='utf-8') as f:
        ret = f.read().splitlines()
    print(f'Load {len(ret):,} from file "{file_name}"')
    return ret


def remove_TLD(dns):
    return [el.split('.')[0] for el in dns]


def input_malignant(output_file, data_dir, nrows=None):
    domain_field = 'domain'
    pattern = f"{data_dir}/*/example_domains.txt"
    files = glob.iglob(pattern, recursive=True)
    print(f"pattern={pattern}")
    out_df = pd.DataFrame()
    for file in files:
        df = pd.read_csv(file, header=None, nrows=nrows, usecols=[0]).rename(columns={0: domain_field})
        print(f"Loaded {file}, {df.shape[0]:,}. Example: {df.loc[0, domain_field]}")
        df = df.drop_duplicates()
        print(f"    Deduplicated: {df.shape[0]:,}")
        
        out_df = pd.concat([out_df, df])
        print(f"    Concatenated {df.shape[0]:,} -> {out_df.shape[0]:,}")
        
    print(f"Result {out_df.shape[0]:,}")
    out_df = out_df.drop_duplicates(subset=[domain_field])
    print(f"Depuplicated by domains {out_df.shape[0]:,}")
    output_file = f"{data_dir}/{output_file[:-4]}.{out_df.shape[0]//1_000_000}M.csv"
    out_df.to_csv(output_file, index=False)
    print(f"Saved  {out_df.shape[0]:,} into {output_file}")
    return out_df


def concatenate_all(files, out_dir, nrows=100):
    df_res = pd.DataFrame()
    for el in files:
        df = pd.read_csv(el["file"], nrows=nrows)
        print(f" Loaded {df.shape[0]:,} {el['file']}, columns: {list(df.columns)}")
        
        if not el['is_domain_extracted']:
            print(f"  Domain extraction...") 
            df["domain"] = df["domain"].apply(lambda d: tldextract.extract(d).domain)
        df['label'] = el['label']
        print(f"  Added the label: {el['label']}")
        
        df_res = pd.concat([df_res, df])
        print(f"  Concatenated {df.shape[0]:,} -> {df_res.shape[0]:,}")
        
        df_res = df_res.drop_duplicates(subset='domain') # Preference to the first samples (to bening)!!!
        print(f"  Deduplicated domains: {df_res.shape[0]:,}") 

    df = df_res
    df = shuffle(df).reset_index(drop=True)
    print('='*40)
    print(f"Shuffled: {df.shape[0]:,}")
    
    out_file = f"{out_dir}/data.csv"
    df.to_csv(out_file, index=False)
    print(f"Saved {df.shape[0]:,} {out_file}")
    return df
