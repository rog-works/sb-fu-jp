#!/bin/bash

dir=$(cd $(dirname $0); pwd)

cd ${dir}/../

python app.py \
--target quests \
--target items \
--discover
