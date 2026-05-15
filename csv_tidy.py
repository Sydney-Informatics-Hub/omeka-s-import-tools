import csv
import sys
from argparse import ArgumentParser
from pathlib import Path
import ftfy

def validate_utf8(r, col, value):
    fixed, explanation = ftfy.fix_and_explain(value)
    if explanation:
        print(
            f"Cleaned text in row {r} col {col}: {explanation}",
            file=sys.stderr
            )
    return fixed

def validate_numeric(r, col, v):
    if v:
        try:
            return float(v)
        except ValueError as e:
            print(f"Bad number in row {r} col {col}: '{v}'")
            return v
    else:
        return ""


def clean(r, row, numeric_cols):
    """I'm conflating validation and cleaning here"""
    clean_row = []
    for col in range(len(row)):
        if col in numeric_cols:
            clean_row.append(validate_numeric(r, col, row[col]))
        else:
            clean_row.append(validate_utf8(r, col, row[col]))
    return clean_row
            

def csv_get_shape(input):
    with open(input, "r", encoding='utf-8-sig') as csfh:
        reader = csv.reader(csfh)
        for row in reader:
            print(len(row))


def csv_trim(input, output, cols, max, numeric_cols):
    rows = []
    r = 0
    with open(input, "r", encoding='utf-8-sig') as csfh:
        reader = csv.reader(csfh)
        for row in reader:
            if max > 0 and r > max:
                print(f"Ending at {r} rows", file=sys.stderr)
                break
            r += 1
            if row[0]:
                if len(row) > cols:
                    row = row[:cols]
                else:
                    if len(row) < cols:
                        for c in range(len(row), cols):
                            row[c] = ''
                clean_row = clean(r, row, numeric_cols)
                rows.append(clean_row)

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
        "--max",
        type=int,
        help="max lines",
        default=0
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
        numeric_cols = []
        if args.numeric:
           numeric_cols = [ int(n) for n in args.numeric.split(',') ]
        print(args.input, args.output, args.cols, args.max, numeric_cols)
        csv_trim(args.input, args.output, args.cols, args.max, numeric_cols)


if __name__ == "__main__":
    main()
