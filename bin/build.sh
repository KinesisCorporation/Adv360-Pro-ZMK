#!/usr/bin/env bash

set -e

PWD=$(pwd)
TIMESTAMP=$(date -u +"%Y%m%d%H%M%S")

# West Init
west init -l config
# West Update
west update
# West Zephyr export
west zephyr-export
# West Build (left)
west build -s zmk/app -d build/left -b adv360_left -- -DZMK_CONFIG="${PWD}/config"
# Adv360 Left DTS File
cat -n build/left/zephyr/adv360_left.dts.pre.tmp
# Adv360 Left Kconfig file
cat build/left/zephyr/.config | grep -v "^#" | grep -v "^$"
# West Build (right)
west build -s zmk/app -d build/right -b adv360_right -- -DZMK_CONFIG="${PWD}/config"
# Adv360 Right DTS File
cat -n build/right/zephyr/adv360_right.dts.pre.tmp
# Adv360 Right Kconfig file
cat build/right/zephyr/.config | grep -v "^#" | grep -v "^$"
# Rename zmk.uf2
cp build/left/zephyr/zmk.uf2 ./firmware/${TIMESTAMP}-left.uf2 && cp build/right/zephyr/zmk.uf2 ./firmware/${TIMESTAMP}-right.uf2
