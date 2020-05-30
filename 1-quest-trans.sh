#!/bin/bash

files=`find fu_assets/quests/ -type f -name '*.questtemplate'`

time python trans.py --dest dest --keys 'text,title,completionText' ${files}

