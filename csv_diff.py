import polars as pl
from argparse import ArgumentParser
from pathlib import Path


def abbrev(v):
    if v is not None:
        return v[:20]
    else:
        return v


def csv_diff(a, b):
    dfa = pl.read_csv(a)
    dfb = pl.read_csv(b)
    cols = dfa.columns
    mismatches = (
        dfa.filter(~dfa.hash_rows().is_in(dfb.hash_rows().implode()))
           .join(dfb, on="ID", how="left", suffix="_dfb")
       )
    for row in mismatches.to_dicts():
        print("-- " + row["ID"])
        for col in cols:
            if f"{col}_dfb" in row:
                va = row[col]
                vb = row[f"{col}_dfb"]
                if va != vb:
                    ava = abbrev(va)
                    avb = abbrev(vb)
                    print(f"   A {col}: '{ava}'")
                    print(f"   B {col}: '{avb}'")



def main():
    ap = ArgumentParser("CSV trim")
    ap.add_argument(
        "-a",
        type=Path,
        help="CSV file A",
    )
    ap.add_argument(
        "-b",
        type=Path,
        help="CSV file B",
    )
    args = ap.parse_args()
    csv_diff(args.a, args.b)


if __name__ == "__main__":
    main()
