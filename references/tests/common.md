# テストの共通仕様

## テスト環境の準備

### フィクスチャ
- 一時ディレクトリの作成と削除
  - `temp_work_dir`：pytestの`tmp_path`を利用
  - テスト終了時に自動的に削除

### モック
- 必要に応じてファイルシステム操作をモック化
- 標準出力・標準エラー出力のキャプチャ（`capsys`）

## テストフレームワークと実行方法

### 使用ツール
- `pytest`：テストフレームワーク
- `pytest-cov`：カバレッジ計測
- `pytest-mock`：モック機能

### テストの実行方法
```bash
# 全テストの実行
pytest tests/ -v

# 特定のテストファイルの実行
pytest tests/test_generate_input.py -v
pytest tests/test_run_calculations.py -v

# カバレッジレポート付きで実行
pytest tests/ --cov=src --cov-report=term-missing
```

## テストコードの方針
- 英語でコメントとdocstringを記述
- NumPyスタイルのdocstringを使用
- テストケースは機能ごとにクラスでグループ化
- 正常系と異常系のテストを明確に区別 
