# HPhi Energy Gap Analysis / HPhiエネルギーギャップ解析

[English](#english) | [日本語](#japanese)

<a id="english"></a>
## Overview
A set of Python scripts to analyze energy gaps from HPhi calculation results. The scripts handle the following tasks:
1. Generate input files for HPhi calculations
2. Run HPhi calculations for different system sizes
3. Analyze energy gaps and perform finite-size scaling

### Physical Model
The scripts analyze the spin-\(S\) antiferromagnetic Heisenberg chain with single-ion anisotropy:

\[
H = J\sum_{i=1}^N \mathbf{S}_i \cdot \mathbf{S}_{i+1} + D\sum_{i=1}^N (S_i^z)^2
\]

where:
- \(J > 0\): Antiferromagnetic coupling (fixed to 1)
- \(D\): Single-ion anisotropy (specified by `--delta` option)
- \(S\): Spin magnitude (specified by `--2S` option as \(2S\))
- \(N\): System size (specified by `--sizes` option)

### Observables
The scripts calculate:
1. Ground state energy \(E_0\)
2. First excited state energy \(E_1\)
3. Energy gap \(\Delta = E_1 - E_0\)
4. Finite-size scaling of the gap:
   \[
   \Delta(N) = \Delta_\infty + \frac{a}{N} + O(N^{-2})
   \]
   where \(\Delta_\infty\) is the gap in the thermodynamic limit.

## Directory Structure
```
.
├── src/
│   ├── generate_input.py    # Generate HPhi input files
│   ├── run_calculations.py  # Execute HPhi calculations
│   └── analyze_results.py   # Analyze energy gaps
├── tests/                   # Test files
├── data/                    # Input data directory (created by generate_input.py)
└── results/                 # Results directory
    └── raw/                # Raw calculation results
```

## Prerequisites
- Python 3.8 or later
- Required Python packages:
  ```
  numpy>=1.24.0
  matplotlib>=3.7.0
  pytest>=7.3.1  # for running tests
  ```
- HPhi (compiled and accessible in PATH)

## Usage

### 1. Generate Input Files
```bash
python src/generate_input.py [options]
  --work-dir DIR    Working directory (default: current directory)
  --2S VALUE        Value of 2S (default: 1)
  --delta VALUE     Value of Δ (default: 1.0)
  --sizes LIST      Comma-separated list of system sizes (default: 4,6,8,10,12)
```

### 2. Run Calculations
```bash
python src/run_calculations.py [options]
  --work-dir DIR    Working directory (default: current directory)
```

### 3. Analyze Results
```bash
python src/analyze_results.py [options]
  --work-dir DIR    Working directory (default: current directory)
  --format FORMAT   Output format for plots: pdf, png, or pdf,png (default: pdf)
```

---

<a id="japanese"></a>
## 概要
HPhi計算結果からエネルギーギャップを解析するためのPythonスクリプト群です。以下の処理を行います：
1. HPhi計算用の入力ファイルの生成
2. 異なるシステムサイズでのHPhi計算の実行
3. エネルギーギャップの解析と有限サイズスケーリング

### 物理模型
スピン\(S\)の反強磁性ハイゼンベルグ鎖に一軸異方性を加えた模型を解析します：

\[
H = J\sum_{i=1}^N \mathbf{S}_i \cdot \mathbf{S}_{i+1} + D\sum_{i=1}^N (S_i^z)^2
\]

ここで：
- \(J > 0\)：反強磁性相互作用（1に固定）
- \(D\)：一軸異方性（`--delta`オプションで指定）
- \(S\)：スピンの大きさ（`--2S`オプションで\(2S\)として指定）
- \(N\)：システムサイズ（`--sizes`オプションで指定）

### 計算する物理量
以下の物理量を計算します：
1. 基底状態エネルギー \(E_0\)
2. 第一励起状態エネルギー \(E_1\)
3. エネルギーギャップ \(\Delta = E_1 - E_0\)
4. ギャップの有限サイズスケーリング：
   \[
   \Delta(N) = \Delta_\infty + \frac{a}{N} + O(N^{-2})
   \]
   ここで\(\Delta_\infty\)は熱力学極限でのギャップ。

## ディレクトリ構成
```
