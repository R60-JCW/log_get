#!/bin/sh
# 2重起動防止シェルにて実行中のプロセスIDをファイルに書きこんでいるので、読み込む
read_PID=$(<./under_test/executing_pid.txt)

# under_test配下にファイルが存在するとと期実行でテスト実行中と判定されるためファイルは削除しておく
rm -f ./under_test/executing_pid.txt

# 読み込んだPIDを終了する
kill -15 "$read_PID"

exit 0
