### 引数 ###
# プレイブック内で、本shell実行時に下記2つの引数を渡して実行する。
# $1 -> 実行トリガー。プレイブック実行時のextra変数で指定した文字列が入る。(例--extra-vars "trigger=SCHEDULER")
# $2 -> 実行日時。プレイブック内の変数を引数として使用する。(YYYYMMDD_HHMMSS)

### 変数 ###
# ディレクトリ
## カレントディレクトリ
CURRENT=$(cd $(dirname $0);pwd)
## ローカルリポジトリ
#REPOSITORY_DIR='tmp_repo/'
REPOSITORY_DIR=$3
## 履歴保存ディレクトリ
DIFF_DIR='Diff_Add_Commit/'

# プレイブック(未使用)
# PLAYBOOK="Configuretaion_Management_main.yml"

# path
## リポジトリフルパス
REPO_PATH="${CURRENT}/${REPOSITORY_DIR}"

## 履歴保存ディレクトリパス
DIFF_PATH="${CURRENT}/${DIFF_DIR}"

# tag
TAG="MASTER"

############

### BODY ###

# 実行日時とトリガーのメッセージ作成
MSG="Done at $2 by $1."

# 差分確認処理
set -e

## リポジトリディレクトリに移動
cd ${REPO_PATH}

## gitのステータスを確認
git add -N .

set +e

## 差分を確認し、差分があれば終了コード1を返す
git diff --exit-code --quiet

## 差分結果の判定
### 終了コードが1であれば
if [[ $? -eq 1 ]]; then

### 1.差分結果の出力メッセージ作成
CHANGE="There ARE changes."
MSG_CHANGE="${MSG} ${CHANGE}"

### 2.diffにより差分があったファイルの行のみ抽出
DIFF=`git diff | grep -e diff -e "@@"`

### 1,2の実行日時、トリガー、差分結果をdiff.logに追記
echo "${MSG_CHANGE} ${DIFF}" >> ${DIFF_PATH}diff.log

### 終了コードが1以外の場合
else

### 差分結果の出力メッセージ作成
NOT_CHANGE="There are NO changes"
MSG_NOT_CHANGE="${MSG} ${NOT_CHANGE}"

### 実行日時、トリガー、変更ない結果をdiff.logに保存
echo "${MSG_NOT_CHANGE}" >> ${DIFF_PATH}diff.log

fi
# 差分確認処理ここまで


# リモートリポジトリへのpush処理
set -e

## git statusコマンドの結果を代入
RESULT=`git status`

## 結果に変更がなければ(リポジトリの更新がない場合)
if [ "`echo $RESULT | grep "working tree clean"`" ] ; then

### 処理終了
exit


## リポジトリに更新があった場合、
else

### ステージに登録
git add .

### 実行日時、トリガーをコミットメッセージに記載
git commit -m "${MSG}"

### リモートリポジトリにpush
git push origin main -n
git push origin main

## コミットコードの代入
commit_code=$(git log --oneline -1 | head -c7)

### コミット履歴を作成。実行日時、トリガー、コミットコードをcommit.logに追記。
echo "${MSG} The commit code is: ${commit_code}" >> ${DIFF_PATH}commit.log

##  マスターコミットとの比較
set +e

## 差分を確認し、差分があれば終了コード1を返す
git diff $TAG $commit_code --exit-code --quiet
#git diff $TAG $TAG --exit-code --quiet

## 差分結果の判定
### 終了コードが1であれば
if [[ $? -eq 1 ]]; then
diff_rlt_msg="マスターログとの差分が発生しています。試験開始前に環境を確認して下さい。"

else
diff_rlt_msg="マスターログとの差分はありません。試験開始可能です。"

fi

## Teamsへの通知
### 変更リポジトリの取得
changed_repo=`git remote -v | grep push | awk -F'/' '{print $NF}' | awk '{print $1}'`

rlt_msg="検証環境の構成に変更が発生しました。変更可箇所はリポジトリ:${changed_repo}のコミットコード:${commit_code}を確認してください。"
#std_rlt_msg=`echo -e ${rlt_msg}`

### 通知実行(メッセージに改行ができないため、通知を2つに分ける)
#curl -X POST http://xx.xx.xx.xx:XXXX/v1/notify/teams \
#curl -X POST http://xx.xx.xx.xx:XXXX/v1/notify/teams \
#  --header 'Content-Type: text/plain' \
#  --data "${rlt_msg}"

curl -X POST --data-urlencode "payload={\"channel\": \"#通知テスト\", \"username\": \"webhookbot\", \"text\": \"${rlt_msg}\", \"icon_emoji\": \":ghost:\"}" https://hooks.slack.com/services/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

#curl -X POST http://xx.xx.xx.xx:XXXX/v1/notify/teams \
#  --header 'Content-Type: text/plain' \
#  --data "${diff_rlt_msg}"
#  --data "test2  \ntest2"
#  --data-raw "検証環境の構成に変更が発生しました。変更可箇所はリポジトリ:${changed_repo}のコミットコード:${commit_code}を確認してください。\\n$diff_rlt_msg"
#echo -e ${rlt_msg} | curl -X POST http://xx.xx.xx.xx:XXXX/v1/notify/teams

curl -X POST --data-urlencode "payload={\"channel\": \"#通知テスト\", \"username\": \"webhookbot\", \"text\": \"${diff_rlt_msg}\", \"icon_emoji\": \":ghost:\"}" https://hooks.slack.com/services/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

fi
# リモートリポジトリへのpush処理ここまで
