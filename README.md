# HPhi Energy Gap Analysis / HPhiエネルギーギャップ解析

[English](#english) | [日本語](#japanese)

<a id="english"></a>
## Overview
A set of Python scripts to analyze energy gaps from HPhi calculation results. The scripts handle the following tasks:
1. Generate input files for HPhi calculations
2. Run HPhi calculations for different system sizes
3. Analyze energy gaps and perform finite-size scaling

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

## ディレクトリ構成
```
.
├── src/
│   ├── generate_input.py    # HPhi入力ファイル生成
│   ├── run_calculations.py  # HPhi計算実行
│   └── analyze_results.py   # エネルギーギャップ解析
├── tests/                   # テストファイル
├── data/                    # 入力データディレクトリ（generate_input.pyにより作成）
└── results/                 # 結果ディレクトリ
    └── raw/                # 生の計算結果
```

## 実行に必要な準備
- Python 3.8以降
- 必要なPythonパッケージ：
  ```
  numpy>=1.24.0
  matplotlib>=3.7.0
  pytest>=7.3.1  # テスト実行用
  ```
- HPhi（コンパイル済みでPATHが通っていること）

## 実行手順

### 1. 入力ファイルの生成
```bash
python src/generate_input.py [オプション]
  --work-dir DIR    作業ディレクトリ（デフォルト：カレントディレクトリ）
  --2S VALUE        2Sの値（デフォルト：1）
  --delta VALUE     Δの値（デフォルト：1.0）
  --sizes LIST      システムサイズのカンマ区切りリスト（デフォルト：4,6,8,10,12）
```

### 2. 計算の実行
```bash
python src/run_calculations.py [オプション]
  --work-dir DIR    作業ディレクトリ（デフォルト：カレントディレクトリ）
```

### 3. 結果の解析
```bash
python src/analyze_results.py [オプション]
  --work-dir DIR    作業ディレクトリ（デフォルト：カレントディレクトリ）
  --format FORMAT   プロット出力形式：pdf、png、または pdf,png（デフォルト：pdf）
``` 
