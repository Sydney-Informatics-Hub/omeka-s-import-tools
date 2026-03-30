import polars as pl
from argparse import ArgumentParser
from pathlib import Path


def csv_diff(a, b):
    dfa = pl.read_csv(a)
    dfb = pl.read_csv(b)
    mismatches = (
        dfa.filter(~dfa.hash_rows().is_in(dfb.hash_rows().implode()))
           .join(dfb, on="ID", how="left", suffix="_dfb")
       )
    return mismatches




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
    with pl.Config() as cfg:
        cfg.set_tbl_cols(-1)
        mismatches = csv_diff(args.a, args.b)
        print(mismatches)


if __name__ == "__main__":
    main()
