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
