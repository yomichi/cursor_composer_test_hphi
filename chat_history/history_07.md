### #7

`generate_input.py` で作る入力ファイルを修正してもらいたい。
答えを知っているので直接指摘した方がいいが、今回はテストなので、ふわっとした指示に対応できるかどうか試してみる。

#### In

- `specification.md`
	- `### スクリプトのオプション` セクションは不要
- `generate_input.py.md`
	- HPhiのスタンダードモードを使う
	- `StdFace.def`
		- LanczosではなくてCGを使うようにしてください
		- SpinではなくてSpinGCであることに注意してください

#### Out

仕様書を更新します。まず`specification.md`から不要なセクションを削除します。

````markdown:references/specification.md
# スピン鎖のエネルギーギャップ計算戦略

// ... existing code ...

## 実装手順

### 1. HPhiの入力ファイル生成
- 異なるサイズ（N = 4, 6, 8, 10, 12など）のスピン鎖に対する入力ファイルを自動生成
  - `StdFace.def`：基本パラメータの設定
    - モデル：`model = "SpinGC"`
    - スピンの大きさ：`2S`の値を指定
    - 格子：1次元鎖
  - `hamiltonian.def`：ハミルトニアンの定義
    - 最近接相互作用のみ
    - XY項の係数：J = 1.0（固定）
    - Z項の係数：J * Δ
  - サイズごとに別のディレクトリを作成

### 2. 計算の実行
// ... existing code ...
````


次に`generate_input.py.md`を更新し、HPhiのスタンダードモードとCG法の使用を明確にします。

````markdown:references/src/generate_input.py.md
# generate_input.py

反強磁性XXZ模型の入力ファイルを生成するスクリプト

## 機能
- 指定されたサイズのスピン鎖に対するHPhiの入力ファイルを生成（スタンダードモード用）
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
model = "SpinGC"      # SpinGCモデル（一般化スピン）
method = "CG"         # 共役勾配法
lattice = "chain lattice"
L = {size}
2S = {2s}
J = 1.0
2Sz = 0              # 全スピンのz成分
nelec = {nelec}      # 粒子数（2S*L/2に設定）
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


主な変更点は以下の通りです：

1. `specification.md`から削除した項目：
   - スクリプトのオプションセクション（各スクリプトの仕様ファイルに移動）

2. `generate_input.py.md`の更新：
   - スタンダードモードの使用を明確化
   - `StdFace.def`の設定を更新
     - `method = "CG"`（Lanczosから変更）
     - `model = "SpinGC"`の説明を追加
     - `nelec`パラメータを追加（SpinGCモデルで必要）

これらの変更により、HPhiのスタンダードモードでSpinGCモデルを正しく使用できるようになりました。実装を始めましょうか？

