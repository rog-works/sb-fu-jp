#!/bin/bash

for dir in `ls -F fu_assets/items | grep /`; do
	files=`find fu_assets/items/${dir} -type f | egrep '(chest|legs|head|item|argument|currency|consumable|instrument)$' | awk -F, '{printf "%s,", $1}'`
	time python trans.py --dest dest --keys 'description' --files "${files}"
done
