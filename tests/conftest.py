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
