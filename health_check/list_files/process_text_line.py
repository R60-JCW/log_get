#!/usr/bin/env python
import copy
import sys

# 加工対象ファイル
tgt_file = sys.argv[1]
new_file = tgt_file + '_processed'

# 削除リスト
del_file = sys.argv[2]


with open(tgt_file) as f:
    tgt_lines = f.read()

with open(del_file) as f:
    del_lines = f.read()




if __name__ == "__main__":
    # 加工対象と削除リストを読み込み、削除リストにある文字列を加工対象から削除
    with open(new_file, mode='w') as f:
        for tgt_line in tgt_lines:
            for del_line in del_lines:
                if del_line in tgt_line:
                    f.write(tgt_line)


