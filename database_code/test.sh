#!/bin/bash
TOTAL_NUM_ROWS=$(wc -l < loader.sql) 
echo $TOTAL_NUM_ROWS
ROWS_WANTED=$(awk "BEGIN {printf \"%.0f\",$1/100*${TOTAL_NUM_ROWS}}")
echo $ROWS_WANTED

head -n $ROWS_WANTED loader.sql > $1_loader.sql