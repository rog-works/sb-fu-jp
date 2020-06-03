#!/bin/bash

for dir in `ls -F fu_assets/items | grep /`; do
	files=`find fu_assets/items/${dir} -type f | egrep '(activeitem|augment|back|beamaxe|chest|consumable|currency|flashlight|harvestingtool|head|instrument|item|legs|liqitem|matitem|miningtool|thrownitem|tillingtool|wiretool)$' | awk -F, '{printf "%s,", $1}'`
	python app.py --dest dest --keys 'description' --files "${files}"
done
