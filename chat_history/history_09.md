### #9

ハルシネーションを起こした結果、よくわからない方向に突っ走りだした。
指示だけで戻すのはしんどそうなので、仕様ファイルを直接書き換える。

```` md
### StdFace.def
```
model = "SpinGC"
method = "CG"
lattice = "chain lattice"
L = {size}
2S = {2s}
h = 0.0
```
````

相互作用

#### In

 `### StdFace.def` を書き換え、不要なパラメータを削除しました。 `delta` を用いて、相互作用パラメータを適切に設定してください。
 また、CG法で第一励起状態を計算するためのパラメータを追加してください。

#### Out

`generate_input.py.md`の`StdFace.def`セクションを更新します。

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
h = 0.0
Jx = 1.0
Jy = 1.0
Jz = {delta}
NOmega = 2
CG_maxIter = 1000
CG_eps = 1e-12
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

`StdFace.def`の主な変更点：

1. XXZ模型のパラメータ設定：
   - `Jx = 1.0`, `Jy = 1.0`：XY平面での相互作用（J=1に固定）
   - `Jz = {delta}`：z方向の相互作用（Δパラメータ）
   - `h = 0.0`：ゼロ磁場

2. CG法による励起状態計算のパラメータ：
   - `NOmega = 2`：基底状態と第一励起状態を計算
   - `CG_maxIter = 1000`：CG法の最大反復回数
   - `CG_eps = 1e-12`：CG法の収束判定条件

3. 不要なパラメータを削除：
   - `J`（個別の`Jx`, `Jy`, `Jz`で指定）
   - `2Sz`（`h = 0.0`で指定）
   - その他の冗長なパラメータ

これで、XXZ模型のハミルトニアンを正しく設定し、CG法で第一励起状態まで計算できる設定になりました。実装を始めましょうか？

