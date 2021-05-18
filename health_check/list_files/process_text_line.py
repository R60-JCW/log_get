#!/usr/bin/env python
import copy
import sys

    if __name__ == "__main__":
    # 加工対象と削除リストを読み込み、削除リストにある文字列を加工対象から削除
    # 加工対象ファイル

    # tgt_file = sys.argv[1]
    tgt_file = 'show_run.log'
    new_file = tgt_file + '_processed'

    # 削除リスト
    # del_file = sys.argv[2]
    del_file = 'show_run_del_list.txt'

    with open(tgt_file) as f:
        tgt_lines = f.readlines()
        #print(tgt_lines)

    with open(del_file) as f:
        del_lines = f.readlines()
        #print(del_lines)
    
    # 削除対象の整理
    del_list = []
    for del_line in del_lines:
        del_line = del_line.strip()
        if del_line == '':
            pass
        else:
            del_list.append(del_line)
        
        #print(del_list)
        with open(new_file, mode='w') as f:
            l = []
            newl =[]
            
            for tgt_line in tgt_lines:
                tgt_line = tgt_line.strip()
                if not any(tgt_line.startswith(dl) for dl in del_list):
                    f.write(tgt_line + '\n')


