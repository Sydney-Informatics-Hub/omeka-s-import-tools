import csv
from argparse import ArgumentParser
from pathlib import Path


def validate_numeric(i, row, num_cols):
    for col in num_cols:
        v = row[col]
        if v:
            try:
                nval = float(v)
            except ValueError as e:
                print(f"Bad number in row {i} col {col}: '{v}'")


def csv_trim(input, output, cols, num_cols):
    rows = []
    i = 0
    with open(input, "r") as csfh:
        reader = csv.reader(csfh, dialect="excel")
        for row in reader:
            if row[0]:
                if len(row) > cols:
                    row = row[:cols]
                else:
                    if len(row) < cols:
                        for i in range(len(row), cols):
                            row[i] = ''
                rows.append(row)
            i += 1
            if i > 1:
                validate_numeric(i, row, num_cols)

    with open(output, "w") as csfh:
        writer = csv.writer(csfh, dialect="excel")
        for row in rows:
            writer.writerow(row)


def main():
    ap = ArgumentParser("CSV trim")
    ap.add_argument(
        "--input",
        type=Path,
        help="Input csv",
    )
    ap.add_argument(
        "--output",
        type=Path,
        help="Output",
    )
    ap.add_argument(
        "--cols",
        type=int,
        help="Number of cols"
    )
    ap.add_argument(
    	"--numeric",
    	type=str,
    	help="Fields to check for numeric values"
    )
    args = ap.parse_args()
    num_cols = []
    if args.numeric:
       num_cols = [ int(n) for n in args.numeric.split(',') ] 
    csv_trim(args.input, args.output, args.cols, num_cols)


if __name__ == "__main__":
    main()
