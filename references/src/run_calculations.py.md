# run_calculations.py

HPhiを用いて各サイズの計算を実行するスクリプト

## 機能
- 指定された作業ディレクトリ内の各サイズのディレクトリでHPhiを実行
- 計算結果を適切なディレクトリに保存
- 計算の進捗状況を表示

## コマンドラインオプション
```
--work-dir DIR    作業ディレクトリ（デフォルト：カレントディレクトリ）
```

## 実行手順
1. 作業ディレクトリ内の`data/N{size}`ディレクトリを検索
2. 各ディレクトリで以下を実行：
   ```bash
   cd data/N{size}
   HPhi -s StdFace.def
   ```
3. 計算結果を`results/raw/N{size}`に移動

## 出力ディレクトリ構造
```
{work_dir}/
├── data/
│   └── N{size}/
│       ├── StdFace.def
│       ├── hamiltonian.def
│       └── output/
└── results/
    └── raw/
        └── N{size}/
            ├── zvo_energy.dat
            └── zvo_phys_Sz.dat
```

## エラー処理
- HPhi実行時のエラー検出
- 計算の収束確認
- 既存の計算結果の取り扱い（バックアップ/スキップ）

## 使用例
```bash
# カレントディレクトリで実行
python src/run_calculations.py

# 作業ディレクトリを指定
python src/run_calculations.py --work-dir ./work
``` 