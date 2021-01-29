#!/bin/sh
# 自身が起動していたら終了
#sh dable_start_check.sh

if [ $$ != `pgrep -fo $0`  ]; then
    echo "[`date '+%Y/%m/%d %T'`] myself is already running. exit myself."
    exit 1
fi

# debug code
# echo "[`date '+%Y/%m/%d %T'`] 実行中"
PID=$$

# echo "$PID"
echo "$PID" >./under_test/executing_pid.txt

# 実行したplaybookがkillコマンドで終了するまで起動させるため、sleepにてタイマー入力
sleep 300
exit 0
