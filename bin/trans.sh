#!/bin/bash

dir=$(cd $(dirname $0); pwd)

cd ${dir}/../

python app.py \
--target a_notyetadded \
--target ai \
--target animations \
--target artwork \
--target aseprite_palettes \
--target bees \
--target behaviors \
--target biomes \
--target celestial \
--target cinematics \
--target collections \
--target cursors \
--target custom \
--target damage \
--target dialog \
--target dungeons \
--target effects \
--target fu_metagui \
--target humanoid \
--target interface \
--target items \
--target leveling \
--target liquids \
--target metagui \
--target monsters \
--target music \
--target names \
--target npcs \
--target objects \
--target parallax \
--target particles \
--target plants \
--target player \
--target projectiles \
--target quests \
--target quickbar \
--target radiomessages \
--target recipes \
--target scripts \
--target sfx \
--target ships \
--target spawners \
--target spawntypes \
--target species \
--target stagehands \
--target stats \
--target tech \
--target tenants \
--target terrain \
--target tiles \
--target tilesets \
--target treasure \
--target vehicles \
--target weather \
--target zb \
--discover

# ignore
# --target a_modders XXX example
# --target codex XXX huge text
