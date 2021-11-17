#!/bin/bash
YEAR_1=$1
YEAR_2=$2
YEAR_3=$3
#LC_ALL=C -F -A 5 -B 5
# Assuming Taxi_Trips.csv is on current directory and only 3 years matter
# Fetchs only the data from given years
head -n 1 Taxi_Trips.csv > new_Taxi_Trips.csv
grep -E "/${YEAR_1}|/${YEAR_2}|/${YEAR_3}" Taxi_Trips.csv >> new_Taxi_Trips.csv