import pandas as pd

def read_data(name):

    if 'csv' in name:
        df = pd.read_csv(name)
    elif 'xls' in name:
        df = pd.read_excel(name)

    else:
        raise ValueError("File type not understood")

    df = df.dropna(axis = 1).rename(columns={"Unnamed: 0": "t"})

    qs = df["t"].apply(
        lambda q: "-Q".join([str(int(n)) for n in q.split(":")])
    )

    df["t"] = pd.PeriodIndex(qs.values, freq = "Q")

    return df.set_index("t")