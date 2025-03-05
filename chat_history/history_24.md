### #24

テストに失敗。

#### In

```
================================================ short test summary info ================================================
FAILED tests/test_run_calculations.py::TestRunHPhi::test_failed_run - Failed: DID NOT RAISE <class 'subprocess.CalledProcessError'>
FAILED tests/test_run_calculations.py::TestMain::test_successful_execution - SystemExit: 1
FAILED tests/test_run_calculations.py::TestMain::test_hphi_error - AssertionError: assert 'Error: Command failed' in 'Error: Output directory not found: /Users/yomichi/tmp/pytest-of-y...
=
```

#### Out

テストの失敗を修正します。主に3つの問題があります：

1. `test_failed_run`: HPhi実行失敗時の例外処理
2. `test_successful_execution`: 出力ディレクトリの作成
3. `test_hphi_error`: エラーメッセージの不一致

```python:tests/conftest.py
"""Common test fixtures."""

import os
import sys
from pathlib import Path
import pytest
import subprocess

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def temp_work_dir(tmp_path):
    """Create a temporary working directory.

    Returns
    -------
    Path
        Path to temporary directory
    """
    return tmp_path


@pytest.fixture
def mock_hphi_success(mocker):
    """Mock successful HPhi execution.

    Returns
    -------
    MagicMock
        Mocked subprocess.run function
    """
    def run_success(*args, **kwargs):
        # Create output directory and dummy file
        calc_dir = Path.cwd()
        output_dir = calc_dir / "output"
        output_dir.mkdir(exist_ok=True)
        (output_dir / "zvo_energy.dat").write_text("dummy energy data")
        
        result = mocker.MagicMock()
        result.returncode = 0
        return result

    mock_run = mocker.patch("subprocess.run", side_effect=run_success)
    return mock_run


@pytest.fixture
def mock_hphi_failure(mocker):
    """Mock failed HPhi execution.

    Returns
    -------
    MagicMock
        Mocked subprocess.run function
    """
    def run_failure(*args, **kwargs):
        if kwargs.get("check", False):
            raise subprocess.CalledProcessError(1, args[0])
        result = mocker.MagicMock()
        result.returncode = 1
        return result

    mock_run = mocker.patch("subprocess.run", side_effect=run_failure)
    return mock_run


@pytest.fixture
def setup_calc_dirs(temp_work_dir):
    """Set up calculation directories with dummy input files.

    Parameters
    ----------
    temp_work_dir : Path
        Temporary working directory

    Returns
    -------
    Path
        Path to working directory
    """
    data_dir = temp_work_dir / "data"
    data_dir.mkdir()

    # Create size directories and dummy input files
    sizes = [4, 6, 8]
    for size in sizes:
        size_dir = data_dir / f"N{size}"
        size_dir.mkdir()
        (size_dir / "StdFace.def").write_text("dummy")

    return temp_work_dir
```


次に、`run_calculations.py`のエラー処理を修正します。

```python:src/run_calculations.py
#!/usr/bin/env python3

"""Run HPhi calculations for different system sizes.

This script executes HPhi calculations for each system size
and organizes the results in a structured directory.
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns
    -------
    argparse.Namespace
        Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Run HPhi calculations for different system sizes"
    )
    parser.add_argument(
        "--work-dir",
        default=".",
        help="Working directory (default: current directory)",
    )
    parser.add_argument(
        "--hphi",
        default="HPhi",
        help="Path to HPhi executable (default: HPhi)",
    )

    return parser.parse_args()


def find_calc_dirs(work_dir: str) -> List[Path]:
    """Find calculation directories.

    Parameters
    ----------
    work_dir : str
        Working directory path.

    Returns
    -------
    List[Path]
        List of calculation directory paths.

    Raises
    ------
    FileNotFoundError
        If data directory or calculation directories are not found.
    """
    work_path = Path(work_dir)
    data_dir = work_path / "data"

    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    calc_dirs = sorted(data_dir.glob("N*"))
    if not calc_dirs:
        raise FileNotFoundError(f"No calculation directories found in {data_dir}")

    return calc_dirs


def run_hphi(calc_dir: Path, hphi: str) -> int:
    """Run HPhi calculation in specified directory.

    Parameters
    ----------
    calc_dir : Path
        Calculation directory path.
    hphi : str
        Path to HPhi executable.

    Returns
    -------
    int
        Return code from HPhi.

    Raises
    ------
    subprocess.CalledProcessError
        If HPhi execution fails.
    """
    current_dir = os.getcwd()
    try:
        os.chdir(calc_dir)
        result = subprocess.run(
            [hphi, "-s", "StdFace.def"],
            check=True,
            capture_output=True,
            text=True
        )
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"HPhi execution failed: {e}", file=sys.stderr)
        raise
    finally:
        os.chdir(current_dir)


def move_results(work_dir: Path, calc_dir: Path) -> None:
    """Move calculation results to results directory.

    Parameters
    ----------
    work_dir : Path
        Working directory path.
    calc_dir : Path
        Calculation directory path.

    Raises
    ------
    FileNotFoundError
        If output directory or energy file is not found.
    """
    output_dir = calc_dir / "output"
    if not output_dir.exists():
        raise FileNotFoundError(f"Output directory not found: {output_dir}")

    energy_file = output_dir / "zvo_energy.dat"
    if not energy_file.exists():
        raise FileNotFoundError(f"Energy file not found: {energy_file}")

    # Create results directory
    size_name = calc_dir.name
    result_dir = work_dir / "results" / "raw" / size_name
    result_dir.mkdir(parents=True, exist_ok=True)

    # Move energy file
    shutil.copy2(energy_file, result_dir / "zvo_energy.dat")


def main():
    """Main function."""
    try:
        args = parse_args()
        work_dir = Path(args.work_dir)

        # Find calculation directories
        calc_dirs = find_calc_dirs(work_dir)

        # Run calculations and move results
        for calc_dir in calc_dirs:
            print(f"Running calculation in {calc_dir}")
            try:
                run_hphi(calc_dir, args.hphi)
                move_results(work_dir, calc_dir)
                print(f"Finished calculation in {calc_dir}")
            except subprocess.CalledProcessError:
                print("Error: Command failed", file=sys.stderr)
                sys.exit(1)
            except FileNotFoundError as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
```


主な修正点：

1. `conftest.py`の修正：
   - `mock_hphi_success`: 出力ディレクトリとファイルを作成
   - `mock_hphi_failure`: `subprocess.CalledProcessError`を正しく発生

2. `run_calculations.py`の修正：
   - `run_hphi`のエラー処理を改善
   - `main`関数での例外処理を具体的に分類
   - エラーメッセージの統一

これらの修正により、以下のテストケースが正しく動作するはずです：
- `test_failed_run`: HPhi実行失敗時に`CalledProcessError`を発生
- `test_successful_execution`: 出力ディレクトリとファイルが正しく作成
- `test_hphi_error`: 正しいエラーメッセージが出力

テストを再実行してください：
```bash
pytest tests/test_run_calculations.py -v
```


