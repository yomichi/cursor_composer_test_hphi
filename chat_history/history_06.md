### #6

スクリプトごとの仕様は別ファイルにしてもらおう。

#### In

- スクリプトごとの仕様ファイルをつくってください
    - 例： `references/src/generate_input.py.md`
- `--2s`, `--delta`は `generate_input.py` のみ必要です
    - それぞれ `--2s=1` と `--delta=1.0` をデフォルト値にします

#### Out

各スクリプトの詳細仕様を作成します。まず`generate_input.py`の仕様から作成します。

````markdown:references/src/generate_input.py.md
# generate_input.py

反強磁性XXZ模型の入力ファイルを生成するスクリプト

## 機能
- 指定されたサイズのスピン鎖に対するHPhiの入力ファイルを生成
- 各サイズごとに専用のディレクトリを作成
- `StdFace.def`と`hamiltonian.def`を生成

## コマンドラインオプション
```
--work-dir DIR    作業ディレクトリ（デフォルト：カレントディレクトリ）
--2s INTEGER      スピンの大きさ2S（デフォルト：1）
--delta FLOAT     イジング異方性Δ（デフォルト：1.0）
--sizes LIST      計算するシステムサイズのリスト（デフォルト：4,6,8,10,12）
```

## 生成するファイル

### StdFace.def
```
model = "SpinGC"
method = "Lanczos"
lattice = "chain lattice"
L = {size}
2S = {2s}
J = 1.0
2Sz = 0
```

### hamiltonian.def
```
======================
NInteraction {N_int}
======================
========i_j_s_tilde====
======================
{interactions}
======================
```
ここで`interactions`は以下の形式の行を含む：
```
i j 1 1.0  # Sx_i Sx_j
i j 2 1.0  # Sy_i Sy_j
i j 3 {delta}  # Sz_i Sz_j
```

## 出力ディレクトリ構造
```
{work_dir}/
└── data/
    ├── N4/
    │   ├── StdFace.def
    │   └── hamiltonian.def
    ├── N6/
    │   ├── StdFace.def
    │   └── hamiltonian.def
    └── ...
```

## エラー処理
- 作業ディレクトリの存在確認・作成
- パラメータの妥当性チェック
  - 2S > 0
  - サイズリストの各要素 > 0
- 既存ファイルの上書き確認

## 使用例
```bash
# デフォルト値を使用（S=1/2, Δ=1.0）
python src/generate_input.py

# S=1, Δ=0のXY模型
python src/generate_input.py --2s 2 --delta 0.0

# カスタムサイズを指定
python src/generate_input.py --sizes 4,6,8

# 作業ディレクトリを指定
python src/generate_input.py --work-dir ./work
```
````


次に`run_calculations.py`の仕様を作成します。

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
````

最後に`analyze_results.py`の仕様を作成します。

````markdown:references/src/analyze_results.py.md
# analyze_results.py

計算結果を解析し、エネルギーギャップのサイズ依存性をプロットするスクリプト

## 機能
- 各サイズの計算結果からエネルギー固有値を読み取り
- エネルギーギャップを計算
- サイズ依存性のプロット生成
- （オプション）有限サイズスケーリング解析

## コマンドラインオプション
```
--work-dir DIR    作業ディレクトリ（デフォルト：カレントディレクトリ）
```

## 入力データ
各サイズのディレクトリから以下のファイルを読み込み：
```
results/raw/N{size}/zvo_energy.dat
```

## 出力データ
1. エネルギーギャップのデータファイル
```
results/raw/energy_gap.dat
# 形式：
# N  E0  E1  Gap
  4  ...  ...  ...
  6  ...  ...  ...
  ...
```

2. プロットファイル
```
results/figures/gap_size_dependence.pdf
# プロット内容：
# - x軸：1/N
# - y軸：エネルギーギャップ
# - エラーバー（該当する場合）
# - フィッティング曲線（オプション）
```

## エラー処理
- 入力ファイルの存在確認
- データの妥当性チェック
  - エネルギー値の順序
  - 欠損データの処理
- プロット生成時のエラー処理

## 使用例
```bash
# カレントディレクトリで実行
python src/analyze_results.py

# 作業ディレクトリを指定
python src/analyze_results.py --work-dir ./work
```
````

3つのスクリプトの仕様を作成しました。各スクリプトの主な特徴は以下の通りです：

1. `generate_input.py`
   - モデルパラメータ（2S, Δ）の設定
   - 入力ファイル（StdFace.def, hamiltonian.def）の生成
   - デフォルト値：2S=1（S=1/2）、Δ=1.0（Heisenberg模型）

2. `run_calculations.py`
   - HPhi実行の制御
   - 計算結果の整理
   - 作業ディレクトリオプションのみ

3. `analyze_results.py`
   - エネルギーギャップの計算
   - プロット生成
   - 作業ディレクトリオプションのみ

これらの仕様に基づいて、実装を進めることができます。どのスクリプトから実装を始めましょうか？


