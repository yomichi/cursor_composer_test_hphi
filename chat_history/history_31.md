### #31

#### In

```
================================================ short test summary info ================================================
FAILED tests/test_analyze_results.py::test_parse_args - SystemExit: 2
FAILED tests/test_analyze_results.py::test_read_energies - ValueError: Both ground state and first excited state must be present
FAILED tests/test_analyze_results.py::test_main - SystemExit: 2
```

#### Out

テストの失敗を修正していきます。3つのテストが失敗していますので、それぞれ原因を分析して修正します。

1. `test_parse_args`と`test_main`の失敗：
   - `SystemExit: 2`は通常、argparseのエラー処理に関連する問題です
   - テスト時にコマンドライン引数の処理が適切に行われていない可能性があります

2. `test_read_energies`の失敗：
   - エネルギー状態の解析に問題があります
   - 正規表現のパターンが適切に状態を抽出できていない可能性があります

まず、テストコードを修正します：

```python:tests/test_analyze_results.py
import pytest
import os
import tempfile
from pathlib import Path
import numpy as np
from analyze_results import (
    parse_args,
    find_result_dirs,
    read_energies,
    calculate_gaps,
    write_gap_data,
    create_plot,
    main
)

@pytest.fixture
def sample_energy_data():
    return """State 0
  Energy  -7.1043675920
  Doublon  0.4164356536
  Sz  0.0000000000

State 1
  Energy  -6.9876543210
  Doublon  0.3987654321
  Sz  0.0000000000
"""

@pytest.fixture
def temp_workdir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

def test_parse_args(temp_workdir):
    # Test default values
    args = parse_args([])
    assert args.work_dir == "."

    # Test custom work directory
    args = parse_args(["--work-dir", str(temp_workdir)])
    assert args.work_dir == str(temp_workdir)

    # Test non-existent directory
    with pytest.raises(SystemExit):
        parse_args(["--work-dir", "/non/existent/path"])

def test_find_result_dirs(temp_workdir):
    # Create test directory structure
    for n in [4, 6, 8]:
        path = temp_workdir / f"results/raw/N{n}"
        path.mkdir(parents=True)
    
    dirs = find_result_dirs(temp_workdir)
    assert len(dirs) == 3
    assert [d.name for d in dirs] == ["N4", "N6", "N8"]

    # Test empty directory
    empty_dir = temp_workdir / "empty"
    empty_dir.mkdir()
    with pytest.raises(ValueError):
        find_result_dirs(empty_dir)

def test_read_energies(temp_workdir, sample_energy_data):
    # Test successful read
    energy_file = temp_workdir / "zvo_energy.dat"
    energy_file.parent.mkdir(parents=True, exist_ok=True)
    energy_file.write_text(sample_energy_data)

    e0, e1 = read_energies(energy_file)
    assert isinstance(e0, float)
    assert isinstance(e1, float)
    assert e0 == pytest.approx(-7.1043675920)
    assert e1 == pytest.approx(-6.9876543210)

    # Test missing file
    with pytest.raises(FileNotFoundError):
        read_energies(temp_workdir / "nonexistent.dat")

    # Test invalid format
    invalid_file = temp_workdir / "invalid.dat"
    invalid_file.write_text("Invalid format")
    with pytest.raises(ValueError):
        read_energies(invalid_file)

    # Test missing state
    incomplete_data = "State 0\n  Energy  -7.1043675920\n"
    incomplete_file = temp_workdir / "incomplete.dat"
    incomplete_file.write_text(incomplete_data)
    with pytest.raises(ValueError):
        read_energies(incomplete_file)

def test_calculate_gaps():
    sizes = [4, 6, 8]
    e0s = [-7.1043675920, -12.1234568, -16.1234568]
    e1s = [-6.9876543210, -11.9876543, -15.9876543]
    
    gaps = calculate_gaps(sizes, e0s, e1s)
    
    assert len(gaps) == 3
    assert all(isinstance(gap, float) for gap in gaps)
    assert gaps[0] == pytest.approx(0.11671327)

    # Test invalid input
    with pytest.raises(ValueError):
        calculate_gaps([4], [-7.0], [-8.0])  # E1 < E0

def test_write_gap_data(temp_workdir):
    sizes = [4, 6, 8]
    e0s = [-7.1043675920, -12.1234568, -16.1234568]
    e1s = [-6.9876543210, -11.9876543, -15.9876543]
    gaps = calculate_gaps(sizes, e0s, e1s)
    
    output_file = temp_workdir / "energy_gap.dat"
    write_gap_data(output_file, sizes, e0s, e1s, gaps)
    
    assert output_file.exists()
    content = output_file.read_text()
    assert "# N" in content
    assert "E0" in content
    assert "E1" in content
    assert "Gap" in content

def test_create_plot(temp_workdir):
    sizes = [4, 6, 8]
    gaps = [0.11671327, 0.13580246, 0.13580246]
    
    plot_file = temp_workdir / "energy_gap.png"
    create_plot(plot_file, sizes, gaps)
    
    assert plot_file.exists()
    assert plot_file.stat().st_size > 0

def test_main(temp_workdir, sample_energy_data):
    # Create test data structure
    for n in [4, 6, 8]:
        result_dir = temp_workdir / f"results/raw/N{n}"
        result_dir.mkdir(parents=True)
        energy_file = result_dir / "zvo_energy.dat"
        energy_file.parent.mkdir(parents=True, exist_ok=True)
        energy_file.write_text(sample_energy_data)
    
    main([str(temp_workdir)])
```


次に、実装コードも修正します：

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
    parser.add_argument('work_dir', nargs='?', default='.',
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
    
    # Parse state blocks
    state_pattern = r'State (\d+)\n(?:.*\n)*?  Energy\s+([+-]?\d+\.\d+)'
    matches = re.finditer(state_pattern, content)
    
    energies = {}
    for match in matches:
        state = int(match.group(1))
        energy = float(match.group(2))
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


主な修正点について説明させていただきます：

1. **コマンドライン引数の処理（`parse_args`）**:
   - `work_dir`を位置引数として扱うように変更
   - `nargs='?'`を追加して省略可能に

2. **エネルギー値の読み込み（`read_energies`）**:
   - 正規表現パターンを改善
   - `State (\d+)\n(?:.*\n)*?  Energy\s+([+-]?\d+\.\d+)`というパターンで、状態番号とエネルギー値を一度に抽出
   - 非貪欲マッチング（`*?`）を使用して適切なブロック解析を実現

3. **テストケースの修正**:
   - `test_parse_args`で実際のディレクトリを使用
   - `test_main`でテストデータの準備を確実に

これらの修正により、以下の問題が解決されるはずです：
- コマンドライン引数の処理エラー
- エネルギー値の解析エラー
- テストケースの実行エラー

テストを再実行すると、すべてのテストがパスするはずです。


