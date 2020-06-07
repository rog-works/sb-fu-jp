#!/bin/bash

dir=$(cd $(dirname $0); pwd)

cd ${dir}/../../

find fu_assets/items/ -type f | egrep '(activeitem|augment|back|beamaxe|chest|consumable|currency|flashlight|harvestingtool|head|instrument|item|legs|liqitem|matitem|miningtool|thrownitem|tillingtool|wiretool)$' > ${dir}/files.txt
