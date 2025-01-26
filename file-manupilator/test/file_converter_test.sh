#!/bin/bash

# 変数の定義
test_pyfile="../  src/file_converter.py"
test_mdfile="./test.md"
result_file="test_result.html"

# 関数の定義
function test_file_converter {
  python3 test_pyfile test_mdfile
}

# 関数の呼び出し
test_file_converter

# スクリプト終了時
exit 0
