#!/bin/bash

dir=$(cd $(dirname $0); pwd)

cd ${dir}/../../

find fu_assets/quests/ -type f -name '*.questtemplate' > ${dir}/files.txt