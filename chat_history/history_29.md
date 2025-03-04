### #29

#### In

`src/analyze_results.py` を作成してください。

#### Out

はい、`src/analyze_results.py`を作成します。テストケースに対応する実装を行います。

```python:src/analyze_results.py
#!/usr/bin/env python3

import argparse
from pathlib import Path
import re
import numpy as np
import matplotlib.pyplot as plt

def parse_args(args=None):
    """Parse command line arguments.

    Parameters
    ----------
    args : list, optional
        List of command line arguments, by default None

    Returns
    -------
    argparse.Namespace
        Parsed command line arguments

    Raises
    ------
    SystemExit
        If the specified work directory does not exist
    """
    parser = argparse.ArgumentParser(description='Analyze HPhi energy results')
    parser.add_argument('--work-dir', default='.',
                       help='Working directory containing results')
    
    parsed_args = parser.parse_args(args)
    work_dir = Path(parsed_args.work_dir)
    
    if not work_dir.exists():
        parser.error(f"Directory not found: {work_dir}")
    
    return parsed_args

def find_result_dirs(work_dir):
    """Find and sort result directories containing HPhi outputs.

    Parameters
    ----------
    work_dir : Path
        Working directory path

    Returns
    -------
    list
        Sorted list of result directory paths

    Raises
    ------
    ValueError
        If no result directories are found
    """
    result_pattern = Path(work_dir) / "results/raw/N*"
    dirs = sorted(Path(work_dir).glob("results/raw/N*"),
                 key=lambda x: int(x.name[1:]))
    
    if not dirs:
        raise ValueError(f"No result directories found in {work_dir}")
    
    return dirs

def read_energies(energy_file):
    """Read energy values from HPhi output file.

    Parameters
    ----------
    energy_file : Path
        Path to zvo_energy.dat file

    Returns
    -------
    tuple
        Ground state energy (E0) and first excited state energy (E1)

    Raises
    ------
    FileNotFoundError
        If the energy file does not exist
    ValueError
        If the file format is invalid or required states are missing
    """
    if not energy_file.exists():
        raise FileNotFoundError(f"Energy file not found: {energy_file}")

    content = energy_file.read_text()
    energies = {}
    
    # Parse state blocks
    state_blocks = re.split(r'\nState \d+\n', content)
    for block in state_blocks:
        if not block.strip():
            continue
            
        # Extract state number and energy
        energy_match = re.search(r'Energy\s+([+-]?\d+\.\d+)', block)
        state_match = re.search(r'State (\d+)', block)
        
        if not energy_match or not state_match:
            continue
            
        state = int(state_match.group(1))
        energy = float(energy_match.group(1))
        energies[state] = energy

    if 0 not in energies or 1 not in energies:
        raise ValueError("Both ground state and first excited state must be present")

    if energies[1] < energies[0]:
        raise ValueError("First excited state energy is lower than ground state energy")

    return energies[0], energies[1]

def calculate_gaps(sizes, e0s, e1s):
    """Calculate energy gaps between ground and first excited states.

    Parameters
    ----------
    sizes : list
        List of system sizes
    e0s : list
        List of ground state energies
    e1s : list
        List of first excited state energies

    Returns
    -------
    list
        Energy gaps for each system size

    Raises
    ------
    ValueError
        If any gap is negative
    """
    gaps = []
    for e0, e1 in zip(e0s, e1s):
        gap = e1 - e0
        if gap < 0:
            raise ValueError(f"Negative energy gap found: {gap}")
        gaps.append(gap)
    return gaps

def write_gap_data(output_file, sizes, e0s, e1s, gaps):
    """Write energy gap data to file.

    Parameters
    ----------
    output_file : Path
        Output file path
    sizes : list
        List of system sizes
    e0s : list
        List of ground state energies
    e1s : list
        List of first excited state energies
    gaps : list
        List of energy gaps
    """
    with open(output_file, 'w') as f:
        f.write("# N      E0          E1          Gap\n")
        for n, e0, e1, gap in zip(sizes, e0s, e1s, gaps):
            f.write(f"{n:3d}     {e0:.8f} {e1:.8f}  {gap:.8f}\n")

def create_plot(output_file, sizes, gaps):
    """Create energy gap plot.

    Parameters
    ----------
    output_file : Path
        Output file path for the plot
    sizes : list
        List of system sizes
    gaps : list
        List of energy gaps
    """
    plt.figure(figsize=(8, 6))
    plt.plot(sizes, gaps, 'o-', label='Energy gap')
    plt.xlabel('System size N')
    plt.ylabel('Energy gap')
    plt.grid(True)
    plt.legend()
    plt.savefig(output_file)
    plt.close()

def main(argv=None):
    """Main function to analyze HPhi results.

    Parameters
    ----------
    argv : list, optional
        Command line arguments, by default None
    """
    args = parse_args(argv)
    work_dir = Path(args.work_dir)

    # Find result directories and extract system sizes
    result_dirs = find_result_dirs(work_dir)
    sizes = [int(d.name[1:]) for d in result_dirs]

    # Read energies from each directory
    e0s = []
    e1s = []
    for d in result_dirs:
        e0, e1 = read_energies(d / "zvo_energy.dat")
        e0s.append(e0)
        e1s.append(e1)

    # Calculate gaps and create outputs
    gaps = calculate_gaps(sizes, e0s, e1s)
    write_gap_data(work_dir / "energy_gap.dat", sizes, e0s, e1s, gaps)
    create_plot(work_dir / "energy_gap.png", sizes, gaps)

if __name__ == "__main__":
    main()
```


実装した`src/analyze_results.py`の主な機能について説明させていただきます：

1. **コマンドライン引数の処理** (`parse_args`)
   - `--work-dir`オプションの処理
   - ディレクトリの存在確認

2. **結果ディレクトリの検索** (`find_result_dirs`)
   - `results/raw/N*`パターンのディレクトリを検索
   - システムサイズでソート

3. **エネルギー値の読み込み** (`read_energies`)
   - `zvo_energy.dat`の解析
   - 正規表現を使用してState 0とState 1のエネルギー値を抽出
   - エラー処理（ファイル不在、不正なフォーマット）

4. **ギャップ計算** (`calculate_gaps`)
   - E₁ - E₀の計算
   - 負のギャップのチェック

5. **出力生成**
   - `write_gap_data`: テキストファイル出力
   - `create_plot`: matplotlib使用したプロット生成

6. **メイン処理** (`main`)
   - 全体の処理フローの制御
   - エラー処理

必要なパッケージは以下の通りです：
- numpy
- matplotlib

これらのパッケージは`requirements.txt`に記載する必要があります。また、テストを実行する際は`pytest`も必要です。


