#!/bin/sh

# 自身が起動していたら終了
if [ $$ != `pgrep -fo lock_playbook.sh` ]; then
    echo "[`date '+%Y/%m/%d %T'`] myself is already running. exit myself."
    exit 1
fi
