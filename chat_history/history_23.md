### #23

テストに失敗したが、見た感じパッケージ不足。必要なものを教えてもらう。

#### In

テスト実行に必要なpythonパッケージを教えて下さい。

#### Out

テストを実行するために必要なパッケージをrequirements.txtとして作成します。

```pip requirements:requirements.txt
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0
```

必要なパッケージとその用途：

1. `pytest`
   - Pythonのテストフレームワーク
   - テストの実行と管理
   - フィクスチャの提供

2. `pytest-cov`
   - コードカバレッジの計測
   - `--cov`オプションの提供

3. `pytest-mock`
   - モックオブジェクトの作成
   - `mocker`フィクスチャの提供
   - HPhi実行のモック化に使用

インストール方法：
```bash
pip install -r requirements.txt
```

これらのパッケージをインストールした後、テストを実行できます：
```bash
# 全テストの実行
pytest tests/ -v

# カバレッジレポート付きで実行
pytest tests/ --cov=src --cov-report=term-missing
```


