#!/bin/bash

# Remove the first line (header) and then process the rest
tail -n +2 test.csv | awk -F, 'BEGIN {OFS=","; print "Index,Label"} {if ($4 == "Student" && $5 == "No Income") print NR, "Positive"; else print NR, "Negative";}' > result.csv
