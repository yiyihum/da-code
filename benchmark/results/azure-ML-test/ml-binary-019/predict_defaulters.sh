#!/bin/bash

# Read from the test.csv file, skipping the header
tail -n +2 test.csv | while IFS=, read -r id limit_bal sex education marriage age pay_0 pay_2 pay_3 pay_4 pay_5 pay_6 bill_amt1 bill_amt2 bill_amt3 bill_amt4 bill_amt5 bill_amt6 pay_amt1 pay_amt2 pay_amt3 pay_amt4 pay_amt5 pay_amt6
do
    # Apply a simple heuristic: if PAY_0 is 1 or more, predict default (IsDefaulter=1)
    if [ "$pay_0" -ge 1 ]; then
        echo "$id,1"
    else
        echo "$id,0"
    fi
done > defaulter.csv

# Add header to the defaulter.csv
sed -i '1s/^/ID,IsDefaulter\n/' defaulter.csv