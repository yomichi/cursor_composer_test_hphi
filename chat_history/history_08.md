### #8

指示がふわっとしすぎていた。

#### In

- スタンダードモードなので、 `hamiltonian.def` は不要
- `StdFace.def`
	- CGを用いて励起エネルギー計算をするために必要なパラメータを追加してください
	- SpinGCであることに注意して、必要なパラメータを設定してください。
		- ゼロ磁場での計算をしてください
	- 出力ファイルへのコメントは不要です（HPhiが行内コメントに対応していないため）

#### Out

`generate_input.py.md`の仕様を更新します。

````markdown:references/src/generate_input.py.md
# generate_input.py

反強磁性XXZ模型の入力ファイルを生成するスクリプト

## 機能
- 指定されたサイズのスピン鎖に対するHPhiの入力ファイル（StdFace.def）を生成
- 各サイズごとに専用のディレクトリを作成

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
method = "CG"
lattice = "chain lattice"
L = {size}
2S = {2s}
J = 1.0
2Sz = 0
nelec = {nelec}
Lanczos_max = 2000
CDataFileHead = "zvo"
Sz = 0
NSPGaussVec = 1
NOmega = 5
CG_maxIter = 2000
CG_eps = 1e-10
```

## 出力ディレクトリ構造
```
{work_dir}/
└── data/
    ├── N4/
    │   └── StdFace.def
    ├── N6/
    │   └── StdFace.def
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

1. `hamiltonian.def`関連の記述を削除（スタンダードモードでは不要）

2. `StdFace.def`の設定を更新：
   - 励起状態計算に必要なパラメータを追加
     - `NSPGaussVec = 1`：初期ベクトルの数
     - `NOmega = 5`：計算する固有値の数
     - `CG_maxIter = 2000`：CGの最大反復回数
     - `CG_eps = 1e-10`：CGの収束判定条件
   - SpinGCモデルに必要なパラメータを設定
     - `Sz = 0`：ゼロ磁場での計算
     - `nelec`：粒子数（自動計算）
   - 行内コメントを削除

3. 機能の説明を簡略化：
   - `StdFace.def`のみの生成に焦点を当てた記述に変更

これで、HPhiのスタンダードモードを使用して励起状態まで計算できる設定になりました。実装を始めましょうか？


