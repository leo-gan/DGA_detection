import argparse

PATTERNS = {
    "koreasys": "appx.koreasys{}.com",
    "winsoft": "app2.winsoft{}.com"
}

def dga(prefix):
    pattern = PATTERNS.get(prefix)
    if not pattern:
        raise ValueError("unsupported pattern {}".format(prefix))

    for i in range(20):
        yield pattern.format(i) 

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix", choices=["winsoft", "koreasys"], default="winsoft")
    args = parser.parse_args()
    domains = list(dga("winsoft")) + list(dga("koreasys"))
    # for domain in dga(args.prefix):
    #     domains
    #     print(domain)
    
    import pandas as pd

    df = pd.DataFrame(data={"domain": domains})
    df = df.drop_duplicates()
    df.to_csv("domains.csv", index=False)
    print(f"Saved {df.shape[0]:,} in domains.csv")
