# Usage
# python verify.py input.csv

import csv
import lob
import os
import sys

sys.path.insert(0, os.path.abspath(__file__+'../../../..'))

lob.api_key = 'test_fc26575412e92e22a926bc96c857f375f8b'

skipFirstLine = True

# Column indices in CSV
address1 = 0
address2 = 1
city = 2
state = 3
postcode = 4
country = 'US'

try:
    sys.argv[1]
except IndexError:
    print("Please provide an input CSV file as an argument.")
    print("Usage: python verify.py <csv-input>")
    sys.exit(1)

# Open input files
inputFile = open(sys.argv[1], 'rU')
csvInput = csv.reader(inputFile)

# Create output files
cwd = os.path.dirname(os.path.abspath(__file__))
errors = open(cwd + '/errors.csv', 'w')
verified = open(cwd + '/verified.csv', 'w')

# Loop through input CSV rows
for idx, row in enumerate(csvInput):
    if skipFirstLine and idx == 0:
        continue

    # sanity check
    sys.stdout.write('.')
    sys.stdout.flush()

    try:
        verifiedAddress = lob.Verification.create(
            address_line1=row[address1],
            address_line2=row[address2],
            address_city=row[city],
            address_state=row[state],
            address_zip=row[postcode],
            address_country=country
        )
    except Exception, e:
        outputRow = ",".join(row) + "," + str(e) + "\n"
        errors.write(outputRow)
else:
    outputRow = verifiedAddress.address.address_line1 + ","
    outputRow += verifiedAddress.address.address_line2 + ","
    outputRow += verifiedAddress.address.address_city + ","
    outputRow += verifiedAddress.address.address_state + ","
    outputRow += verifiedAddress.address.address_zip + "\n"
    verified.write(outputRow)

errors.close()
verified.close()
print "\n"