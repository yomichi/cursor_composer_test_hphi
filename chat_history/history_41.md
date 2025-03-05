### #41

#### In

模型の説明が間違っています。 `references/specification.md` を参考にして修正してください。

#### Out

はい、申し訳ありません。`specification.md`に記載されているXXZ模型の説明に修正します。

````markdown:README.md
# HPhi Energy Gap Analysis / HPhiエネルギーギャップ解析

[English](#english) | [日本語](#japanese)

<a id="english"></a>
## Overview
A set of Python scripts to analyze energy gaps from HPhi calculation results. The scripts handle the following tasks:
1. Generate input files for HPhi calculations
2. Run HPhi calculations for different system sizes
3. Analyze energy gaps and perform finite-size scaling

### Physical Model
The scripts analyze the spin-\(S\) antiferromagnetic XXZ chain:

\[
H = J\sum_{i=1}^N \left[ S_{i}^x S_{i+1}^x + S_{i}^y S_{i+1}^y + \Delta S_{i}^z S_{i+1}^z \right]
\]

where:
- \(J > 0\): Antiferromagnetic coupling (fixed to 1)
- \(\Delta\): Ising anisotropy (specified by `--delta` option)
- \(S\): Spin magnitude (specified by `--2S` option as \(2S\))
- \(N\): System size (specified by `--sizes` option)

### Observables
The scripts calculate:
1. Ground state energy \(E_0\)
2. First excited state energy \(E_1\)
3. Energy gap \(\Delta E = E_1 - E_0\)
4. Finite-size scaling of the gap:
   \[
   \Delta E(N) = \Delta E_\infty + \frac{a}{N} + O(N^{-2})
   \]
   where \(\Delta E_\infty\) is the gap in the thermodynamic limit.

// ... rest of English section ...

---

<a id="japanese"></a>
## 概要
HPhi計算結果からエネルギーギャップを解析するためのPythonスクリプト群です。以下の処理を行います：
1. HPhi計算用の入力ファイルの生成
2. 異なるシステムサイズでのHPhi計算の実行
3. エネルギーギャップの解析と有限サイズスケーリング

### 物理模型
スピン\(S\)の反強磁性XXZ鎖を解析します：

\[
H = J\sum_{i=1}^N \left[ S_{i}^x S_{i+1}^x + S_{i}^y S_{i+1}^y + \Delta S_{i}^z S_{i+1}^z \right]
\]

ここで：
- \(J > 0\)：反強磁性相互作用（1に固定）
- \(\Delta\)：イジング異方性（`--delta`オプションで指定）
- \(S\)：スピンの大きさ（`--2S`オプションで\(2S\)として指定）
- \(N\)：システムサイズ（`--sizes`オプションで指定）

### 計算する物理量
以下の物理量を計算します：
1. 基底状態エネルギー \(E_0\)
2. 第一励起状態エネルギー \(E_1\)
3. エネルギーギャップ \(\Delta E = E_1 - E_0\)
4. ギャップの有限サイズスケーリング：
   \[
   \Delta E(N) = \Delta E_\infty + \frac{a}{N} + O(N^{-2})
   \]
   ここで\(\Delta E_\infty\)は熱力学極限でのギャップ。

// ... 残りの日本語セクション ...
````

主な修正点について説明させていただきます：

1. **ハミルトニアンの修正**:
   - 一軸異方性項 \(D\sum_i (S_i^z)^2\) を削除
   - XXZ模型の正しいハミルトニアン（XY項とイジング項）に変更

2. **パラメータの説明の修正**:
   - \(D\)（一軸異方性）を\(\Delta\)（イジング異方性）に変更
   - パラメータの物理的な意味をより正確に記述

3. **記号の統一**:
   - エネルギーギャップを\(\Delta\)から\(\Delta E\)に変更（イジング異方性\(\Delta\)との混同を避けるため）
   - 熱力学極限のギャップも同様に\(\Delta E_\infty\)に変更

4. **用語の統一**:
   - 英語：「Ising anisotropy」
   - 日本語：「イジング異方性」

これにより、`specification.md`に記載された物理模型と整合する説明になりました。


