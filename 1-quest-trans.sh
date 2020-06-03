#!/bin/bash

files=`find fu_assets/quests/ -type f -name '*.questtemplate' | awk -F, '{printf "%s,", $1}'`

time python app.py --dest dest --keys 'text,title' --files "${files}"
