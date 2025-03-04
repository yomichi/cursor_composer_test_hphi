# スピン鎖のエネルギーギャップ計算戦略

## 目的
- スピン鎖のエネルギーギャップのサイズ依存性を、厳密対角化ソルバーHPhiを用いて計算する
- 結果を可視化し、有限サイズスケーリング解析を行う

## 物理系
反強磁性XXZ模型：

$$H = J \sum_i \left[ S_{i}^x S_{i+1}^x + S_{i}^y S_{i+1}^y + \Delta S_{i}^zS_{i+1}^z \right]$$

### パラメータ
- \(S\)：スピンの大きさ（S = 1/2, 1, 3/2, ...）
- \(\Delta\)：イジング異方性
- \(J > 0\)：反強磁性的な結合定数（J = 1に固定）

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
- 各サイズに対してHPhiを実行
  - `HPhi -s StdFace.def`でスタンダードモードで実行
  - 低エネルギー固有値を計算（基底状態と第一励起状態）
  - 並列計算の活用を検討

### 3. 結果の解析
- 各サイズの計算結果から以下を抽出：
  - 基底状態エネルギー E₀
  - 第一励起状態エネルギー E₁
  - エネルギーギャップ Δ = E₁ - E₀

### 4. データ処理とプロット
- Pythonスクリプトで以下を実装：
  - 結果ファイルの読み込み
  - エネルギーギャップの計算
  - サイズ依存性のプロット
    - x軸：1/N（システムサイズの逆数）
    - y軸：エネルギーギャップ Δ
  - 必要に応じて外挿によるバルク極限の推定

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

## 注意点
1. メモリ使用量の考慮
   - システムサイズに応じて必要なメモリ量が指数関数的に増加
   - スピンの大きさSに応じて状態数が増大（(2S+1)^N）
   - 利用可能なリソースに応じて最大サイズを設定

2. 計算効率
   - HPhi の OpenMP 並列化を活用
   - 計算時のスレッド数を適切に設定

3. エラー処理
   - パラメータの妥当性チェック
     - 2Sは正の整数
     - Δは実数
   - 計算の収束確認
   - 異常終了時のエラーハンドリング

4. 作業ディレクトリの管理
   - 絶対パスと相対パスの適切な処理
   - 既存ディレクトリの存在確認とバックアップ
   - 一時ファイルの適切な管理 