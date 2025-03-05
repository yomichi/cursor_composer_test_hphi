### #21

#### In

テストコードを実装してください

#### Out

`run_calculations.py`のテストコードを実装します。まず、共通のフィクスチャを作成し、その後テストコードを実装します。

```python:tests/conftest.py
"""Common test fixtures."""

import os
import sys
from pathlib import Path
import pytest

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
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value.returncode = 0
    return mock_run


@pytest.fixture
def mock_hphi_failure(mocker):
    """Mock failed HPhi execution.

    Returns
    -------
    MagicMock
        Mocked subprocess.run function
    """
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value.returncode = 1
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


次に、`run_calculations.py`のテストコードを実装します。

```python:tests/test_run_calculations.py
"""Test suite for run_calculations.py."""

import os
import sys
from pathlib import Path
import pytest
import subprocess

import run_calculations


def create_args(work_dir=".", hphi="HPhi"):
    """Create an argparse.Namespace object with given parameters.

    Parameters
    ----------
    work_dir : str, optional
        Working directory path, by default "."
    hphi : str, optional
        Path to HPhi executable, by default "HPhi"

    Returns
    -------
    argparse.Namespace
        Arguments namespace
    """
    class Args:
        pass
    
    args = Args()
    args.work_dir = work_dir
    args.hphi = hphi
    return args


class TestParseArgs:
    """Test command line argument parsing."""

    def test_default_values(self, capsys):
        """Test default values of command line arguments."""
        test_args = ["prog"]
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(sys, "argv", test_args)
            args = run_calculations.parse_args()
        
        assert args.work_dir == "."
        assert args.hphi == "HPhi"

    def test_custom_values(self, capsys):
        """Test custom values for command line arguments."""
        test_args = [
            "prog",
            "--work-dir", "work",
            "--hphi", "/usr/local/bin/HPhi"
        ]
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(sys, "argv", test_args)
            args = run_calculations.parse_args()
        
        assert args.work_dir == "work"
        assert args.hphi == "/usr/local/bin/HPhi"


class TestFindCalcDirs:
    """Test calculation directory search."""

    def test_find_dirs(self, setup_calc_dirs):
        """Test finding calculation directories."""
        work_dir = setup_calc_dirs
        calc_dirs = run_calculations.find_calc_dirs(work_dir)
        
        expected = [
            work_dir / "data" / f"N{size}"
            for size in [4, 6, 8]
        ]
        assert calc_dirs == expected

    def test_no_data_dir(self, temp_work_dir):
        """Test when data directory does not exist."""
        with pytest.raises(FileNotFoundError):
            run_calculations.find_calc_dirs(temp_work_dir)

    def test_empty_data_dir(self, temp_work_dir):
        """Test when data directory is empty."""
        data_dir = temp_work_dir / "data"
        data_dir.mkdir()
        
        with pytest.raises(FileNotFoundError):
            run_calculations.find_calc_dirs(temp_work_dir)


class TestRunHPhi:
    """Test HPhi execution."""

    def test_successful_run(self, setup_calc_dirs, mock_hphi_success):
        """Test successful HPhi execution."""
        calc_dir = setup_calc_dirs / "data" / "N4"
        result = run_calculations.run_hphi(calc_dir, "HPhi")
        
        assert result == 0
        mock_hphi_success.assert_called_once()

    def test_failed_run(self, setup_calc_dirs, mock_hphi_failure):
        """Test failed HPhi execution."""
        calc_dir = setup_calc_dirs / "data" / "N4"
        
        with pytest.raises(subprocess.CalledProcessError):
            run_calculations.run_hphi(calc_dir, "HPhi")


class TestMoveResults:
    """Test result file movement."""

    def test_move_results(self, setup_calc_dirs):
        """Test moving result files."""
        work_dir = setup_calc_dirs
        calc_dir = work_dir / "data" / "N4"
        
        # Create dummy output file
        output_dir = calc_dir / "output"
        output_dir.mkdir()
        energy_file = output_dir / "zvo_energy.dat"
        energy_file.write_text("dummy energy data")

        # Move results
        run_calculations.move_results(work_dir, calc_dir)

        # Check if file was moved correctly
        result_file = work_dir / "results" / "raw" / "N4" / "zvo_energy.dat"
        assert result_file.exists()
        assert result_file.read_text() == "dummy energy data"

    def test_no_output(self, setup_calc_dirs):
        """Test when output directory does not exist."""
        work_dir = setup_calc_dirs
        calc_dir = work_dir / "data" / "N4"
        
        with pytest.raises(FileNotFoundError):
            run_calculations.move_results(work_dir, calc_dir)


class TestMain:
    """Test main function."""

    def test_successful_execution(self, setup_calc_dirs, mock_hphi_success, capsys):
        """Test successful execution of main function."""
        test_args = [
            "prog",
            "--work-dir", str(setup_calc_dirs)
        ]
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(sys, "argv", test_args)
            run_calculations.main()

        # Check if result files were created
        for size in [4, 6, 8]:
            result_file = setup_calc_dirs / "results" / "raw" / f"N{size}" / "zvo_energy.dat"
            assert result_file.parent.exists()

    def test_hphi_error(self, setup_calc_dirs, mock_hphi_failure, capsys):
        """Test error handling when HPhi fails."""
        test_args = [
            "prog",
            "--work-dir", str(setup_calc_dirs)
        ]
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(sys, "argv", test_args)
            with pytest.raises(SystemExit) as exc_info:
                run_calculations.main()
            assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Error: Command failed" in captured.err
```


テストコードを2つのファイルに分けて実装しました：

1. `tests/conftest.py`
   - 共通のフィクスチャを定義
   - `temp_work_dir`：一時ディレクトリ
   - `mock_hphi_success`/`mock_hphi_failure`：HPhi実行のモック
   - `setup_calc_dirs`：計算ディレクトリの準備

2. `tests/test_run_calculations.py`
   - コマンドライン引数のパース
   - 計算ディレクトリの検索
   - HPhi実行のテスト
   - 結果ファイルの移動
   - メイン処理の実行

主な特徴：
- 各機能をクラスでグループ化
- 正常系と異常系のテストを実装
- モックを使用してHPhiの実行をシミュレート
- フィクスチャを活用してテスト環境を準備

次のステップとして、`run_calculations.py`の実装を始めましょうか？


