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

def csv_get_shape(input):
    with open(input, "r", encoding='utf-8-sig') as csfh:
        reader = csv.reader(csfh)
        for row in reader:
            print(len(row))

def csv_trim(input, output, cols, num_cols):
    rows = []
    i = 0
    with open(input, "r", encoding='utf-8-sig') as csfh:
        reader = csv.reader(csfh)
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

    with open(output, "w", encoding="utf8") as csfh:
        writer = csv.writer(csfh, dialect="unix")
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
        "--shape",
        action='store_true'
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
    if args.shape:
        csv_get_shape(args.input)
    else:
        num_cols = []
        if args.numeric:
           num_cols = [ int(n) for n in args.numeric.split(',') ] 
        csv_trim(args.input, args.output, args.cols, num_cols)


if __name__ == "__main__":
    main()
