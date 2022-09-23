from datetime import datetime, timedelta
import base64 
import argparse 

def dga(d, day_index, tld_index):
    # tlds = [".com", ".org", ".net", ".info"]
    d -= timedelta(days=day_index)
    ds = d.strftime("%d%m%Y").encode()
    return base64.b64encode(ds).decode().lower().replace("=","a")  # + tlds[tld_index]

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="date for which to generate domains")
    args = parser.parse_args()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()
    domains = []
    for i in range(200000):
        # print(dga(d, i%10, i//10))
        domains.append(dga(d, i, i//10))

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
