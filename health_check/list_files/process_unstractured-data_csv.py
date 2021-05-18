import pandas as pd
import csv
import os
import sys
import textfsm

'''
    <本スクリプト実行方法>
    実行コマンド：python3 process_unstractured-data_csv cmd_log template_file delete-list_file repository_dirname
        コマンドライン第1引数：加工対象ログファイル
        コマンドライン第2引数：加工対象ログ内のコマンドに対応したtemplateファイル
        コマンドライン第3引数：加工対象ログの削除箇所を記載したリストファイル
        コマンドライン第4引数：加工対象ログの保存先リポジトリディレクトリ名


    <スクリプト内容説明>        
    テキストファイルを加工するためのスクリプト
        加工のために、構造データへの変換処理と加工処理の2処理を行う

    構造化データへの変換処理：テンプレートファイルを利用し、非構造化データを構造化データへ変換
        パーサー：textFSM
        input: 加工対象ログ
               加工対象ログに対応するテンプレートファイル
        output:加工対象ログ(csv形式へ変換)

    加工処理：の構造化データを、削除リストに従い削除を実行
        input: 加工対象ログ(csv形式)
               削除リストファイル
        output:加工対象ログ(削除済み)
               加工結果ファイル
'''


# 構造化データ用関数ここから
def start_marking_structured(data_file_path, template_file_path):
    '''
    結果ファイルへ確認開始の記載
    1ファイルへ処理対象ファイルごとにマーキング
    '''
    global result_file

    # 対象コマンドの変数作成
    tgt_cmd = os.path.splitext(os.path.basename(data_file_path))[0]


    with open(result_file, mode='a') as f:
        print('###############################################################################################', file=f)
        print('# 対象コマンド：', tgt_cmd, file=f)
        print('## 構造化データ化処理開始', file=f)
        print('### 構造化対象ファイル  :「', data_file_path,'」及び、', file=f)
        print('### templateファイル：「', template_file_path,'」の確認結果', file=f)


def end_marking_structured():
    '''
    結果ファイルへ確認終了の記載
    '''
    global result_file

    with open(result_file, mode='a') as f:
        print('## 構造化データ化処理終了', file=f)


def read_file_all(data_file_path):
    '''
    加工対象ファイルを読み込み、戻り値に格納
    '''
    global result_file

    # 加工対象ファイルの存在確認
    if not os.path.isfile(data_file_path):
        with open(result_file, mode='a') as f:
            print('##### 【ファイル無し】「', data_file_path, '」が存在しません。', file=f)
            print('「', data_file_path, '」のファイルがありませんでした。')
        end_marking_structured()
        exit()


    # 加工対象の読み込み
    with open(data_file_path, 'r') as f:
        datas = f.read()
        return datas

def template_file_check(template_file_path):
    '''
    templateファイルの存在確認
    '''
    global result_file

    # templateファイルの存在確認
    if not os.path.isfile(template_file_path):
        with open(result_file, mode='a') as f:
            print('##### 【ファイル無し】「', template_file_path, '」が存在しません。', file=f)
            print('「', template_file_path, '」のファイルがありませんでした。')
        end_marking_structured()
        exit()


def read_template_file_and_parse(data_file_path, template_file_path, unstractured_date):
    '''
    templateファイルを読み込み、戻り値に格納
    '''
    global result_file
    # 加工対象の読み込み
    with open(template_file_path, 'r') as f:
        try:
            fsm = textfsm.TextFSM(f)
        except textfsm.parser.TextFSMTemplateError as e:
            with open(result_file, mode='a') as f:
                print('#####【内容確認】「', template_file_path,'」にTextFSMTemplateError：', file=f)
                print('#####',e, file=f)
            end_marking_structured()
            exit()
        except Exception  as e:
            with open(result_file, mode='a') as f:
                print('#####【内容確認】「', template_file_path, '」にError：', file=f)
                print('#####', e, file=f)
            end_marking_structured()
            exit()
        else:
            fsm_data = textfsm.TextFSM(f)
            structured_data = fsm.ParseText(unstractured_date)
            
            #加工前ファイルの保存
            new_file_path = data_file_path.replace('.log', '_before.'+new_extension)
            with open(new_file_path, 'w', newline='') as f:
                w = csv.writer(f)
                w.writerow(fsm_data.header)
                w.writerows(structured_datas)

            return fsm_data, structured_data

def change_extension_and_save_fms(data_file_path, new_extension, fsm_data, structured_datas):
    '''
    templateファイルを読み込み、構造化データへ変換
    変換後、加工対象ファイルの拡張子を変更して保存
    '''
    # 加工対象ファイルの拡張子を変更
    new_file_path = data_file_path.replace('.log', '_after.'+new_extension)

    # 新拡張子で構造化データの保存
    with open(new_file_path, 'w', newline='') as f: # Windowsの場合、空行が入ってしまうため、newline=''が必要
        w = csv.writer(f)
        w.writerow(fsm_data.header)
        w.writerows(structured_datas)

    # 元の加工対象ファイル削除
    # os.remove(data_file_path)
    return new_file_path


# 構造化データ用関数ここまで

# 加工処理用関数ここから
def start_marking_process(data_file_path, delete_list_file_path):
    '''
    結果ファイルへ確認開始の記載
    1ファイルへ処理対象ファイルごとにマーキング
    '''
    global result_file

    with open(result_file, mode='a') as f:
        print('## 加工処理開始', file=f)
        print('### 加工対象ファイル  :「', data_file_path,'」及び、', file=f)
        print('### 削除リストファイル：「', delete_list_file_path,'」の確認結果(記載なければ問題なし)', file=f)


def end_marking_process():
    '''
    結果ファイルへ確認終了の記載
    '''
    global result_file

    with open(result_file, mode='a') as f:
        print('## 加工処理終了', file=f)


def read_list_file_to_list(delete_list_file_path):
    '''
    削除リストファイルを読み込み、戻り値に格納
    先頭のコメントアウトと空白行をを削除した行をリスト化
    '''
    global result_file

    # 削除リストの存在確認
    if not os.path.isfile(delete_list_file_path):
        with open(result_file, mode='a') as f:
            print('##### 【ファイル無し】「', delete_list_file_path, '」が存在しません。', file=f)
            print('「', delete_list_file_path, '」のファイルがありませんでした。')
            end_marking_process()
            exit()

    # 削除リストの読み込み
    with open(delete_list_file_path, 'r') as f:
        # 先頭のコメントアウトを除外した削除用リストの作成
        delete_lists = [s.strip() for s in f.readlines() if not s.startswith('#')]
        # 空白要素の削除
        delete_lists = [i for i in delete_lists if i != '']
        # print('delete_listsは', delete_lists)
        return delete_lists


def read_data_file_to_df(data_file_path):
    '''
    加工対象ファイルを読み込み、戻り値に格納
    読み込み元拡張子  ：  csv形式
    読み込み形式     ：  pandas DateFrame
    '''
    global result_file

    # 削除対象ファイルの読み込み
    if not os.path.isfile(data_file_path):
        with open(result_file, mode='a') as f:
            print('#####【ファイル無し】「', data_file_path, '」が存在しません。', file=f)
            print('「', data_file_path, '」のファイルがありませんでした。')
        end_marking_process()
        exit()

    # 削除元データの読み込み(pandas.Dataframe)(値が数値の場合抽出不可のため、文字列にキャストする)
    df = pd.read_csv(data_file_path, dtype='str')
    return df


def delete_list_count(delete_lists, delete_list_file_path):
    '''
    削除リストの要素が1つもない場合の処理
    削除リストから空白行とコメントアウト行を除いた要素のカウントし、
    1つもない場合は処理中止
    '''
    global result_file

    if len(delete_lists) == 0:
        with open(result_file, mode='a') as f:
            print('##### 【内容確認】', delete_list_file_path, 'に削除対象の記載なし', file=f)
        print('「', delete_list_file_path, '」へ削除対象の記載がありませんでした。結果ファイルを確認してください。')
        end_marking_process()
        exit()


def delimiter_check(delete_lists, delimiter_symbol):
    '''
    区切り文字部分割したときに、行削除用のラベルに複数の記載があった場合の処理
    区切り文字で分割し3つ以上カウントしたら、その行は削除対象から除外
    削除したリストを戻り値とする
    '''
    global result_file

    # 区切り文字分割し、列と行の2要素以外(要素が3つ以上カウント)の場合のリストを作成
    delimiter_check_list = []
    delimiter_check_list = [j for j in delete_lists if len(j.split(delimiter_symbol)) > 2]
    if len(delimiter_check_list) > 0:
        # print('del_listsは', del_lists)
        with open(result_file, mode='a') as f:
            print('#####【内容確認】削除リストファイルに、同一行に区切り文字が複数記載：', delimiter_check_list, file=f)
        # 削除リストから区切り文字複数要素リストにあるものを削除
        [delete_lists.remove(j) for j in delimiter_check_list if j in delete_lists]
    return delete_lists


def column_list_no_value(row_delete_lists, delimiter_symbol):
    '''
    区切り文字部で分割したときに、行削除用のラベルに値が入っていない場合の処理
    区切り文字で分割し値が空白だった場合、その行は削除対象から除外
    削除した行削除用リストを戻り値とする
    '''
    global result_file

    # 行削除用に値が入っていない行削除用の新たなリストの作成
    row_del_list_no_value = [r for r in row_delete_lists if r.split(delimiter_symbol)[1] == ""]
    if len(row_del_list_no_value) > 0:
        with open(result_file, mode='a') as f:
            print('#####【内容確認】削除リストファイルに、行削除箇所の値が記載なし：', row_del_list_no_value, file=f)
        # 行ラベルが空白の場合はリストから削除
        [row_delete_lists.remove(r) for r in row_del_list_no_value if r in row_delete_lists]
        #row_del_list = [l for l in row_del_list if l.split('&')[1] != '']
    return row_delete_lists


def duplicate_check_column(column_delete_list):
    '''
    列削除用リストに重複する要素が含まれている場合の処理
    重複する要素のみのリストを作成し、削除リストから重複を取り除く
    重複を取り除いた列削除用リストを戻り値とする
    '''
    global result_file

    duplicate_col_list = [m for m in set(column_delete_list) if column_delete_list.count(m) > 1]
    if len(duplicate_col_list) > 0:
        # 重複を避けたリストに変換
        column_delete_list = set(column_delete_list)
        with open(result_file, mode='a') as f:
            print('#####【内容確認】削除リストファイルに、列削除用の列ラベルが重複:', duplicate_col_list, file=f)
    return column_delete_list


def duplicate_check_row(row_delete_list):
    '''
    行削除用リストに重複する要素が含まれている場合の処理
    重複する要素のみのリストを作成し、行削除リストから重複を取り除く
    重複を取り除いた行削除用リストを戻り値とする
    '''
    global result_file

    # 行の重複
    duplicate_row_list = [q for q in set(row_delete_list) if row_delete_list.count(q) > 1]
    if len(duplicate_row_list) > 0:
        # 重複を避けたリストに変換
        row_delete_list = set(row_delete_list)
        with open(result_file, mode='a') as f:
            print('#####【内容確認】削除リストファイルに、行削除行の列&行ラベルが重複:', duplicate_row_list, file=f)
    return row_delete_list


def duplicate_check_column_in_row_list(row_delete_list, delimiter_symbol, col_delete_list):
    '''
    行削除用リストに、列削除用リストと重複する列ラベルが含まれている場合の処理
    重複する要素のみのリストを作成し、行削除リストから重複を取り除く
    重複を取り除いた行削除用リストを戻り値とする
    '''
    # 行削除の行で、列が重複
    # 行の列を抽出
    row_del_list_only_col = [n.split(delimiter_symbol)[0] for n in row_delete_list]
    # 列と行削除の列との比較で、お互いのリストに重複があったものをリストに格納
    list_diff = set(col_delete_list) & set(row_del_list_only_col)

    # 重複に該当する行削除用のリスト作成
    list_diff_in_row_del_list = []
    if len(list_diff) > 0:
        # 行削除リストから重複箇所の抽出
        for o in row_delete_list:
            list_diff_in_row_del_list += [o for p in list_diff if p in o]
        # 重複を省いたリストに変換
        [row_delete_list.remove(r) for r in list_diff_in_row_del_list if r in row_delete_list]
        with open(result_file, mode='a') as f:
            print('#####【削除不可】削除リストファイルに、行削除用の列ラベルが列削除用の列ラベルと重複:', list_diff_in_row_del_list, file=f)
            print('#####            行の削除には別の列ラベルを指定してください。', file=f)

    return row_delete_list


def delete_column_is_in_data_file(col_delete_list, df):
    '''
    列削除用リストが加工対象ファイルに含まれているかの確認
    加工対象ファイルに存在しない列ラベルの要素のリストを作成し、あれば列削除リストから取り除く
    存在しない列ラベルを取り除いた列削除用リストを戻り値とする
    '''
    # 列の削除
    # 元データにない列ラベルを削除リストに記載している場合
    global critical_error_cnt
    global result_file

    no_hit_col = [s for s in col_delete_list if s not in df.columns]
    if len(no_hit_col) > 0:
        # print('削除前のcol_del_listは',col_del_list)
        with open(result_file, mode='a') as f:
            print('#####【削除不可】削除リストファイル内、列削除用の列ラベルが加工対象ファイルになし：', no_hit_col, file=f)
        [col_delete_list.remove(l) for l in no_hit_col if l in col_delete_list]
        # print('削除後のcol_del_listは',col_del_list)
        critical_error_cnt += 1
    return col_delete_list, critical_error_cnt


def delete_column_in_row_ilst_is_in_data_file(row_delete_list, delimiter_symbol, df):
    # 行削除リストから列がヒットしていない場合
    global critical_error_cnt
    global result_file

    if len(row_delete_list) == 0:
        return
    del_row_no_hit_col = [t for t in row_delete_list if t.split(delimiter_symbol)[0] not in df.columns]
    if len(del_row_no_hit_col) > 0:
        with open(result_file, mode='a') as f:
            print('#####【削除不可】削除リストファイル内、行削除用の列ラベルが加工対象ファイルになし：', del_row_no_hit_col, file=f)
        [row_delete_list.remove(t) for t in del_row_no_hit_col if t in row_delete_list]
        # print('削除後row_del_listは',row_del_list )
        critical_error_cnt += 1
    return row_delete_list, critical_error_cnt


def delete_row_in_row_ilst_is_in_data_file(row_delete_list, delimiter_symbol, df):
    # 行削除リストから列がヒットし、行がヒットしない場合
    # 行削除リストで列がヒットする要素の抽出
    global critical_error_cnt
    global result_file
    del_row_hit_col = [u for u in row_delete_list if u.split(delimiter_symbol)[0] in df.columns]
    if len(del_row_hit_col) > 0:
        # 行削除リストで列はヒットするが、行はヒットしないリスト
        del_row_hit_col_not_hit_row = [v for v in del_row_hit_col if v.split(delimiter_symbol)[1] not in df[v.split(delimiter_symbol)[0]].values]
        if len(del_row_hit_col_not_hit_row) > 0:
            # 削除リストからは除外
            [row_delete_list.remove(v) for v in del_row_hit_col_not_hit_row if v in row_delete_list]
            with open(result_file, mode='a') as f:
                print('#####【削除不可】削除リストファイル内、行削除用の行ラベルが加工対象ファイルになし：', del_row_hit_col_not_hit_row, file=f)
            critical_error_cnt += 1
    return row_delete_list, critical_error_cnt


def delete_target_line_duplicate(row_delete_list, delimiter_symbol, df):
    # 列、行ラベルともに存在するが、削除対象の行が重複している場合
    # 重複は削除対象外とする
    global critical_error_cnt
    global result_file
    dup_tgt_row_list = []
    # 重複行の辞書を作成
    dup_row_num_dic = make_duplicate_dictionary(row_delete_list, delimiter_symbol, df)
    # 重複行が存在した場合は、削除実行するとエラーが起きるので、行削除のリストからは省く
    if len(dup_row_num_dic) > 0:
        # print(dup_row_num_dic)
        dup_row_line_cnt = len(dup_row_num_dic)
        # 重複辞書から行削除リストに一致した要素をリスト化する
        #delete_tgt_row_list = []
        dup_tgt_row_list = [k for k, v in dup_row_num_dic.items() if k in row_delete_list]

        # 行削除リストから一致した要素を削除
        [row_delete_list.remove(k) for k in dup_tgt_row_list if k in row_delete_list]
        critical_error_cnt += 1
    return row_delete_list, critical_error_cnt, dup_tgt_row_list

def recalculate_row_num(dup_tgt_row_list, delimiter_symbol, df):
    global result_file
    # 削除後の行番号再取得
    dup_row_num_dic = make_duplicate_dictionary(dup_tgt_row_list, delimiter_symbol, df)
    # 重複行の行番号を結果ファイルへ記載
    if len(dup_row_num_dic) > 0:
        with open(result_file, mode='a') as f:
            print('#####【削除不可】削除リストファイルの行削除の対象に、加工対象データの削除行が同一{該当行：行番号}', dup_row_num_dic, file=f)
    return


def make_duplicate_dictionary(row_delete_list, delimiter_symbol, df):
    row_num_zisho = {}
    for x in row_delete_list:
        del_col = x.split(delimiter_symbol)[0]
        del_row = x.split(delimiter_symbol)[1]
        del_num = (df.loc[df[del_col] == del_row].index[0]) + 2 # 行番号は0からの採番、csvにしたときのヘッダー分を含めるので+2
        # rowリストと行番号の辞書作成
        row_num_zisho[x] = del_num

    # 重複行の判定：辞書のkey,valueを１つずつ取得し、値(行番号)が同一かつキーが異なる組み合わせを辞書に登録
    dup_row_num_dic = {}
    for k, v in row_num_zisho.items():
        for l, w in row_num_zisho.items():
            if v == w and k != l:
                dup_row_num_dic[l] = w
    return dup_row_num_dic
    # 加工処理用関数ここまで

def main():
    # 構造化データ化ここから
    global data_file
    global tpl_file
    global result_file
    global save_ext

    # 結果ファイルへ処理開始のマーキング
    start_marking_structured(data_file, tpl_file)
    # print(data_file, tpl_file)

    # 加工対象データ読み込み
    datas = read_file_all(data_file)
    # print(datas)

    # templateファイルの存在確認
    template_file_check(tpl_file)

    # templateファイルの読み込みとデータ解析
    fsm, parsed_data = read_template_file_and_parse(data_file, tpl_file, datas)
    # print(fsm)

    # 解析データの保存(拡張子が変わるので、変更後の加工元データファイルを取得)
    data_file = change_extension_and_save_fms(data_file, save_ext, fsm, parsed_data)

    end_marking_structured()

    # 構造化データ化ここまで


    # 加工処理ここから
    global del_list_file
    global delimiter_symbol
    global critical_error_cnt

    # 処理上、記載不備などで削除ができていない場合は、確認メッセージを出す
    #  critical_error_cntが0の場合はエラーがないと判断、1以上の場合は確認メッセージの対象
    #critical_error_cnt = 0

    # 前回のresultファイルの削除!!!!!!!! Ansibleで実装する !!!!!!!!
    # if os.path.isfile(result_file):
    #   os.remove(result_file)

    # 結果ファイルへ処理開始のマーキング
    start_marking_process(data_file, del_list_file)

    # 削除リストの読み込み(to list)
    del_lists = []
    del_lists = read_list_file_to_list(del_list_file)
    # print(del_lists)

    # 加工対象データの読み込み(to pandas dataframe)
    raw_df = read_data_file_to_df(data_file)
    # print(raw_df)

    # 削除リスト単体の表記チェックここから
    # 区切り文字の確認：&が複数ある場合
    del_lists = delimiter_check(del_lists, delimiter_symbol)

    # 削除対象の有無を確認
    delete_list_count(del_lists, del_list_file)
    # print(del_lists)
    # 削除リスト単体の表記チェックここまで

    # 加工元データと削除リストとの整合性確認ここから
    # 列削除用のリスト作成
    col_del_lists = []
    col_del_lists = [k for k in del_lists if len(k.split(delimiter_symbol)) == 1]

    # 確認の途中でリストが存在しなくなる可能性があるため、存在した場合のみ実施する
    if col_del_lists:
        # 列削除用リストの重複チェック
        # print(col_del_lists)
        col_del_lists = duplicate_check_column(col_del_lists)
        # print(col_del_lists)

        # 列削除用の列ラベルが加工対象に存在するかの確認
        # print(col_del_lists)
        col_del_lists, critical_error_cnt = delete_column_is_in_data_file(col_del_lists, raw_df)
        # print(col_del_lists)
        # print(critical_error_cnt)

    # 列の削除実行
    if col_del_lists:
        # print(raw_df.columns)
        col_deleted_df = raw_df.drop(col_del_lists, axis=1)
        # print(col_deleted_df.columns)

        # 列を削除したdfから行を削除するための別df作成
        deleted_df = col_deleted_df
        # print(deleted_df)
    else:
        deleted_df = raw_df

    # 行削除用のリスト作成
    row_del_lists = []
    row_del_lists = [l for l in del_lists if len(l.split(delimiter_symbol)) == 2]

    # 行削除用に値が入っているかの確認
    if row_del_lists:
        # print(row_del_lists)
        row_del_lists = column_list_no_value(row_del_lists, delimiter_symbol)
        # print(row_del_lists)

        # 行削除用リストの重複チェック
        # print(row_del_lists)
        row_del_lists = duplicate_check_row(row_del_lists)
        # print(row_del_lists)

    if row_del_lists:
        # 行削除用の列ラベルが加工対象に存在するかの確認
        # print(row_del_lists)
        row_del_lists, critical_error_cnt = delete_column_in_row_ilst_is_in_data_file(row_del_lists, delimiter_symbol,
                                                                                      deleted_df)
        # print(row_del_lists)
        # print(critical_error_cnt)

    if row_del_lists:
        # 行削除用の行ラベルが加工対象に存在するかの確認
        # print(row_del_lists)
        row_del_lists, critical_error_cnt = delete_row_in_row_ilst_is_in_data_file(row_del_lists, delimiter_symbol,
                                                                                   deleted_df)
        # print(row_del_lists)
        # print(critical_error_cnt)

    if row_del_lists:
        # 削除対象が加工対象の行に重複があるかの確認
        dup_row_line_cnt = 0
        # print(row_del_lists)
        row_del_lists, critical_error_cnt, duplicate_list = delete_target_line_duplicate(row_del_lists,
                                                                                         delimiter_symbol, deleted_df)
        # print(row_del_lists)
        # print(critical_error_cnt)


    if col_del_lists and row_del_lists:
        # 行削除用リストの列ラベルと、列削除用の列ラベルとの重複チェック
        # print(row_del_lists)
        row_del_lists = duplicate_check_column_in_row_list(row_del_lists, delimiter_symbol, col_del_lists)
        # print(row_del_lists)

    # 加工元データと削除リストとの整合性確認ここまで

    # 行の削除実行
    if row_del_lists:
        for t in row_del_lists:
            del_col_str = t.split(delimiter_symbol)[0]
            del_row_str = t.split(delimiter_symbol)[1]
            deleted_df = deleted_df[deleted_df[del_col_str] != del_row_str]
        # print(deleted_df)

        # 削除してもインデックスは変わらないため、再度振り直し
        deleted_df = deleted_df.reset_index(drop=True)
        # print(deleted_df)

        # 削除後に行番号が変わってしまうので、再度行番号を取得し、エラー箇所を結果ファイルへ記載
        # print(duplicate_list)
        recalculate_row_num(duplicate_list, delimiter_symbol, deleted_df)

    # 削除を実行できないエラーを含む場合、確認メッセージを出す。
    if critical_error_cnt > 0:
        print('削除を実行できないエラーあり。結果ファイルを確認してください。')

    # 保存
    #deleted_df.to_csv('new_env_after_delete.csv', index=False)
    deleted_df.to_csv(data_file, index=False)


    end_marking_process()
    # 加工処理ここまで


if __name__ == '__main__':
    ### global変数の定義
    # 加工元データファイル
    # data_file = r'new_env.txt'
    data_file = sys.argv[1]

    # templateファイル
    tpl_file = sys.argv[2]

    # 行列削除用リストファイルパス
    # del_list_file = r'show_env_delete-list_col_row.txt'
    del_list_file = sys.argv[3]

    # 加工対象ログファイル保存ディレクトリ名
    # repo_dir_name = sys.argv[4]

    # playbook格納ディレクトリ
    #root_dir = '~/test-automation/health-check/'

    # リポジトリディレクトリパス
    #repo_dir_path = root_dir + repo_dir_name

    # 加工元データファイルパス


    # 削除リスト内の列要素と行要素の区切り文字
    delimiter_symbol = '&'

    # 加工後の拡張子
    save_ext = 'csv'

    # エラーカウンタ
    critical_error_cnt = 0

    # 削除結果ファイル
    result_file = 'process_result_file.txt'
    ### global変数の定義 ここまで

    # 本体実行
    main()
    
