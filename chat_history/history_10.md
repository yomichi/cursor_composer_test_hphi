### #10

相互作用は良くなったが、励起状態計算のパラメータについてはハルシネーションが取れないので、手で書き換える `exct = 2`。
また、`run_calculation.py.md` に謎の `zvo_phys_Sz.dat` があるので、これについて尋ねる

#### In

- `generate_input.py.md`
	- `StdFace.def` の仕様をこちらで修正したので確認してください
- `run_calcualtion.py.md`
	- `zvo_phys_Sz.dat` とはなんでしょうか？

#### Out

はい、以下の点を確認・修正します。

1. `generate_input.py.md`の`StdFace.def`の仕様：
   - `NOmega`ではなく`exct = 2`を使用して2つの固有値を計算
   - CG法の詳細パラメータ（`CG_maxIter`、`CG_eps`）は不要
   - その他のパラメータは適切に設定されています

2. `run_calculations.py.md`について：
   - `zvo_phys_Sz.dat`は不要です（磁化の計算結果ファイルで、今回は使用しません）
   - エネルギー固有値は`zvo_energy.dat`のみで十分です

`run_calculations.py.md`を修正します：

````markdown:references/src/run_calculations.py.md
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
│       └── output/
└── results/
    └── raw/
        └── N{size}/
            └── zvo_energy.dat  # 基底状態と第一励起状態のエネルギー
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
````

主な変更点：

1. 出力ファイルの整理：
   - `zvo_phys_Sz.dat`を削除（不要なファイル）
   - `zvo_energy.dat`のみを結果として保存
   - `zvo_energy.dat`の説明を追加（基底状態と第一励起状態のエネルギー）

2. ディレクトリ構造の簡略化：
   - 必要なファイルのみを表示
   - 出力構造をより明確に

これで、エネルギーギャップ計算に必要な出力ファイルのみに焦点を当てた仕様になりました。実装を始めましょうか？


