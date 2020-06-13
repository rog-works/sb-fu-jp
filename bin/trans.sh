#!/bin/bash

cwd=$(cd $(dirname $0); pwd)

cd ${cwd}/../

python app.py \
--target quests \
--target items \
--discover
