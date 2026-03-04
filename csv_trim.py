import csv


with open("CSVs/MarchWorkshop/Locations.csv", "r") as csfh:
    reader = csv.reader(csfh, dialect="excel")
    for row in reader:
        print(len(row))

