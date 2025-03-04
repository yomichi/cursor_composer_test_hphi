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