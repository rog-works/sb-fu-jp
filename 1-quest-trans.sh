#!/bin/bash

for dir in `ls -F fu_assets/quests | grep /`; do
	files=`find fu_assets/quests/${dir} -type f -name '*.questtemplate' | awk -F, '{printf "%s,", $1}'`
	python app.py --dest dest --keys 'text,title' --files "${files}"
done

files=`ls fu_assets/quests/*.questtemplate | awk -F, '{printf "%s,", $1}'`
python app.py --dest dest --keys 'text,title' --files "${files}"
