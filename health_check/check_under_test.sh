
# README以外のファイルを確認して、存在しなければ試験中のテストは無しと判断する
# RESULT=$(ls /home/rundeck/test-automation/health-check/under_test | grep -v README.md)

# shell実行パスの取得
SCRIPT_DIR=$(cd $(dirname $0); pwd)

# ディレクトリに指定のファイル以外の存在確認のファイル格納
RESULT=$(ls $SCRIPT_DIR/under_test | grep -v README.md)

if [ -z "$RESULT" ]; then
  echo $RESULT 
  echo "実行中テストなし"
  exit 0
else
  echo $RESULT
  echo "実行中テストあり"
  exit 1
fi
