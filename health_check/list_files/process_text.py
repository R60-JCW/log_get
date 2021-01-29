#!/usr/bin/env python
import copy
import sys

# 加工対象ファイル
tgt_file = sys.argv[1]

# 削除リスト
del_file = sys.argv[2]


with open(tgt_file) as f:
    tgt_lists = [s.strip() for s in f.readlines()]

with open(del_file) as f:
    del_lists = [s.strip() for s in f.readlines()]


if __name__ == "__main__":
    # 加工対象と削除リストを読み込み、削除リストにある文字列を加工対象から削除
    for tgt_list in tgt_lists:
        for del_list in del_lists:
            if del_list in tgt_list:
                tgt_lists.remove(tgt_list)

    with open(sys.argv[1], mode='w') as f:
        for d in tgt_lists:
            f.write("%s\n" % d)

