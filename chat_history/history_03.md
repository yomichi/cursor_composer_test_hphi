### #3

環境変数は使わなくていい

#### In

- 作業ディレクトリの指定は引数ではなくて `--work-dir` オプションにする
- 作業ディレクトリのデフォルトはカレントディレクトリにする
- 環境変数による指定は不要

#### Out

作業ディレクトリの指定方法を修正します。

```` md
# スピン鎖のエネルギーギャップ計算戦略

// ... existing code ...

## ファイル構成
```
project/
└── src/
    ├── generate_input.py   # 入力ファイル生成スクリプト
    ├── run_calculations.py # 計算実行スクリプト
    └── analyze_results.py  # 結果解析・プロットスクリプト
```

### 作業ディレクトリの設定
- スクリプトは `--work-dir` オプションで作業ディレクトリを指定可能
- デフォルトではカレントディレクトリを使用
- 作業ディレクトリ内に必要なサブディレクトリを自動生成
  ```
  # ディレクトリ構造の例（work-dir="./work"の場合）
  work/
  ├── data/
  │   └── N{size}/
  │       ├── StdFace.def
  │       └── hamiltonian.def
  └── results/
      ├── raw/
      │   └── N{size}/
      │       └── output.dat
      └── figures/
          └── gap_size_dependence.pdf
  ```

### スクリプトの使用例
```bash
# カレントディレクトリを作業ディレクトリとして使用
python src/generate_input.py

# 特定のディレクトリを作業ディレクトリとして指定
python src/generate_input.py --work-dir ./work
```

## 注意点

// ... existing code ...
````

仕様書を更新し、以下の変更を行いました：

1. 作業ディレクトリの指定方法を変更
   - `--work-dir` オプションによる指定に統一
   - デフォルトをカレントディレクトリに変更
   - 環境変数による指定を削除

2. ファイル構成の簡略化
   - プロジェクトディレクトリには `src` のみを含める
   - 作業ディレクトリは任意の場所に作成可能であることを明確化

3. 使用例を追加
   - デフォルト（カレントディレクトリ）での実行例
   - `--work-dir` オプションを使用した実行例

この設計により、以下のような柔軟な使用が可能になります：

1. カレントディレクトリで直接実行する場合：
```bash
cd /path/to/working/directory
python /path/to/project/src/generate_input.py
```

2. 別のディレクトリを作業ディレクトリとして指定する場合：
```bash
python /path/to/project/src/generate_input.py --work-dir /path/to/working/directory
```

次のステップとして、これらの仕様に基づいたスクリプトの実装を始めることができます。どのスクリプトから実装を始めましょうか？

