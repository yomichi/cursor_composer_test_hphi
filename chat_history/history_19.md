### #19

#### In

`run_calculations.py` のテストコードを実装してください

#### Out

`run_calculations.py`のテストコードを実装します。


``` python
"""Test suite for run_calculations.py."""

import os
import sys
import subprocess
from pathlib import Path
import pytest
from typing import List

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import run_calculations


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
def mock_hphi(mocker):
    """Mock HPhi command execution.

    Returns
    -------
    MagicMock
        Mocked subprocess.run function
    """
    mock = mocker.patch("subprocess.run")
    mock.return_value.returncode = 0
    return mock


@pytest.fixture
def sample_calculation_dir(temp_work_dir):
    """Create a sample calculation directory structure.

    Parameters
    ----------
    temp_work_dir : Path
        Temporary working directory

    Returns
    -------
    Path
        Path to the working directory
    """
    data_dir = temp_work_dir / "data"
    data_dir.mkdir()

    # Create size directories with StdFace.def
    for size in [4, 6, 8]:
        size_dir = data_dir / f"N{size}"
        size_dir.mkdir()
        (size_dir / "StdFace.def").write_text("model = \"SpinGC\"")

    return temp_work_dir


class TestParseArgs:
    """Test command line argument parsing."""

    def test_default_values(self, capsys):
        """Test default values of command line arguments."""
        test_args = ["prog"]
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(sys, "argv", test_args)
            args = run_calculations.parse_args()
        
        assert args.work_dir == "."

    def test_custom_values(self, capsys):
        """Test custom values for command line arguments."""
        test_args = ["prog", "--work-dir", "work"]
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(sys, "argv", test_args)
            args = run_calculations.parse_args()
        
        assert args.work_dir == "work"


class TestFindCalculationDirs:
    """Test calculation directory search."""

    def test_find_directories(self, sample_calculation_dir):
        """Test finding calculation directories."""
        dirs = run_calculations.find_calculation_dirs(sample_calculation_dir)
        expected = [
            sample_calculation_dir / "data" / f"N{size}"
            for size in [4, 6, 8]
        ]
        assert dirs == expected

    def test_directory_sorting(self, sample_calculation_dir):
        """Test directory sorting order."""
        # Create directories in random order
        sizes = [8, 4, 12, 6]
        data_dir = sample_calculation_dir / "data"
        for size in sizes:
            size_dir = data_dir / f"N{size}"
            size_dir.mkdir(exist_ok=True)
            (size_dir / "StdFace.def").write_text("")

        dirs = run_calculations.find_calculation_dirs(sample_calculation_dir)
        sizes_found = [int(d.name[1:]) for d in dirs]
        assert sizes_found == sorted(sizes)

    def test_no_data_directory(self, temp_work_dir):
        """Test error when data directory does not exist."""
        with pytest.raises(FileNotFoundError):
            run_calculations.find_calculation_dirs(temp_work_dir)

    def test_no_calculation_directories(self, temp_work_dir):
        """Test error when no calculation directories exist."""
        data_dir = temp_work_dir / "data"
        data_dir.mkdir()
        
        with pytest.raises(FileNotFoundError):
            run_calculations.find_calculation_dirs(temp_work_dir)


class TestRunHPhi:
    """Test HPhi execution."""

    def test_successful_execution(self, sample_calculation_dir, mock_hphi):
        """Test successful HPhi execution."""
        calc_dir = sample_calculation_dir / "data" / "N4"
        run_calculations.run_hphi(calc_dir)
        
        mock_hphi.assert_called_once()
        args, kwargs = mock_hphi.call_args
        assert args[0] == ["HPhi", "-s", "StdFace.def"]
        assert kwargs["cwd"] == calc_dir

    def test_execution_failure(self, sample_calculation_dir, mock_hphi):
        """Test HPhi execution failure."""
        mock_hphi.return_value.returncode = 1
        calc_dir = sample_calculation_dir / "data" / "N4"
        
        with pytest.raises(subprocess.CalledProcessError):
            run_calculations.run_hphi(calc_dir)


class TestMoveResults:
    """Test result file movement."""

    def test_move_results(self, sample_calculation_dir):
        """Test moving result files."""
        calc_dir = sample_calculation_dir / "data" / "N4"
        
        # Create dummy output file
        output_dir = calc_dir / "output"
        output_dir.mkdir()
        (output_dir / "zvo_energy.dat").write_text("1.0")

        # Move results
        run_calculations.move_results(calc_dir, sample_calculation_dir)

        # Check if file was moved correctly
        result_file = sample_calculation_dir / "results" / "raw" / "N4" / "zvo_energy.dat"
        assert result_file.exists()
        assert result_file.read_text() == "1.0"

    def test_missing_output(self, sample_calculation_dir):
        """Test error when output directory is missing."""
        calc_dir = sample_calculation_dir / "data" / "N4"
        
        with pytest.raises(FileNotFoundError):
            run_calculations.move_results(calc_dir, sample_calculation_dir)


class TestMain:
    """Test main function."""

    def test_successful_execution(self, sample_calculation_dir, mock_hphi, capsys):
        """Test successful execution of main function."""
        test_args = ["prog", "--work-dir", str(sample_calculation_dir)]
        
        # Create output files
        for size in [4, 6, 8]:
            calc_dir = sample_calculation_dir / "data" / f"N{size}"
            output_dir = calc_dir / "output"
            output_dir.mkdir()
            (output_dir / "zvo_energy.dat").write_text("1.0")

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(sys, "argv", test_args)
            run_calculations.main()

        # Check if results were moved
        for size in [4, 6, 8]:
            result_file = sample_calculation_dir / "results" / "raw" / f"N{size}" / "zvo_energy.dat"
            assert result_file.exists()

    def test_error_handling(self, temp_work_dir, capsys):
        """Test error handling in main function."""
        test_args = ["prog", "--work-dir", str(temp_work_dir)]
        
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(sys, "argv", test_args)
            with pytest.raises(SystemExit) as exc_info:
                run_calculations.main()
            assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Error:" in captured.err
```

テストコードを実装しました。主な特徴：

1. フィクスチャ
   - `temp_work_dir`：一時ディレクトリの作成
   - `mock_hphi`：HPhi実行のモック化
   - `sample_calculation_dir`：テスト用のディレクトリ構造作成

2. テストクラス
   - `TestParseArgs`：コマンドライン引数の処理
   - `TestFindCalculationDirs`：計算ディレクトリの検索
   - `TestRunHPhi`：HPhi実行の制御
   - `TestMoveResults`：結果ファイルの移動
   - `TestMain`：統合テスト

3. テストケース
   - 正常系：期待通りの動作確認
   - 異常系：エラー処理の確認
   - エッジケース：境界条件の確認

4. モックの活用
   - `subprocess.run`のモック化でHPhiの実行をシミュレート
   - 標準出力・エラー出力のキャプチャ

このテストコードを実行するには、まず`run_calculations.py`の実装が必要です。実装を始めましょうか？


