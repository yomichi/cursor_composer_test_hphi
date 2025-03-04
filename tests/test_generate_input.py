"""Test suite for generate_input.py."""

import os
import sys
from pathlib import Path
import pytest
from typing import List

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import generate_input


@pytest.fixture
def temp_work_dir(tmp_path):
    """Create a temporary working directory.

    Returns
    -------
    Path
        Path to temporary directory
    """
    return tmp_path


def create_args(work_dir=".", two_s=1, delta=1.0, sizes=None):
    """Create an argparse.Namespace object with given parameters.

    Parameters
    ----------
    work_dir : str, optional
        Working directory path, by default "."
    two_s : int, optional
        Value of 2S, by default 1
    delta : float, optional
        Value of Delta, by default 1.0
    sizes : List[int], optional
        List of system sizes, by default [4,6,8,10,12]

    Returns
    -------
    argparse.Namespace
        Arguments namespace
    """
    if sizes is None:
        sizes = [4, 6, 8, 10, 12]
    
    class Args:
        pass
    
    args = Args()
    args.work_dir = work_dir
    args.two_s = two_s
    args.delta = delta
    args.sizes = sizes
    return args


class TestParseArgs:
    """Test command line argument parsing."""

    def test_default_values(self, capsys):
        """Test default values of command line arguments."""
        test_args = ["prog"]
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(sys, "argv", test_args)
            args = generate_input.parse_args()
        
        assert args.work_dir == "."
        assert args.two_s == 1
        assert args.delta == 1.0
        assert args.sizes == [4, 6, 8, 10, 12]

    def test_custom_values(self, capsys):
        """Test custom values for command line arguments."""
        test_args = [
            "prog",
            "--work-dir", "work",
            "--2s", "2",
            "--delta", "0.5",
            "--sizes", "4,6,8"
        ]
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(sys, "argv", test_args)
            args = generate_input.parse_args()
        
        assert args.work_dir == "work"
        assert args.two_s == 2
        assert args.delta == 0.5
        assert args.sizes == [4, 6, 8]

    def test_invalid_sizes(self, capsys):
        """Test error handling for invalid sizes format."""
        test_args = ["prog", "--sizes", "4,6,invalid"]
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(sys, "argv", test_args)
            with pytest.raises(SystemExit):
                generate_input.parse_args()


class TestValidateParameters:
    """Test parameter validation."""

    def test_valid_parameters(self):
        """Test validation with valid parameters."""
        args = create_args(two_s=2, delta=0.5, sizes=[4, 6, 8])
        generate_input.validate_parameters(args)  # Should not raise

    def test_invalid_two_s(self):
        """Test validation with invalid 2S value."""
        args = create_args(two_s=0)
        with pytest.raises(ValueError, match="2S must be positive"):
            generate_input.validate_parameters(args)

    def test_invalid_sizes(self):
        """Test validation with invalid sizes."""
        args = create_args(sizes=[4, 0, 8])
        with pytest.raises(ValueError, match="All sizes must be positive"):
            generate_input.validate_parameters(args)


class TestSetupDirectories:
    """Test directory setup."""

    def test_create_directories(self, temp_work_dir):
        """Test creation of directory structure."""
        sizes = [4, 6, 8]
        generate_input.setup_directories(temp_work_dir, sizes)

        data_dir = temp_work_dir / "data"
        assert data_dir.exists()
        assert data_dir.is_dir()

        for size in sizes:
            size_dir = data_dir / f"N{size}"
            assert size_dir.exists()
            assert size_dir.is_dir()

    def test_existing_directories(self, temp_work_dir):
        """Test handling of existing directories."""
        sizes = [4, 6]
        
        # Create directories first time
        generate_input.setup_directories(temp_work_dir, sizes)
        
        # Try creating again - should not raise
        generate_input.setup_directories(temp_work_dir, sizes)


class TestGenerateStdface:
    """Test StdFace.def content generation."""

    def test_content_format(self):
        """Test format of generated content."""
        content = generate_input.generate_stdface(4, 1, 1.0)
        
        # Check required parameters
        assert 'model = "SpinGC"' in content
        assert "method = \"CG\"" in content
        assert "lattice = \"chain lattice\"" in content
        assert "L = 4" in content
        assert "2S = 1" in content
        assert "h = 0.0" in content
        assert "Jx = 1.0" in content
        assert "Jy = 1.0" in content
        assert "Jz = 1.0" in content
        assert "exct = 2" in content

    def test_parameter_values(self):
        """Test different parameter values."""
        content = generate_input.generate_stdface(6, 2, 0.5)
        assert "L = 6" in content
        assert "2S = 2" in content
        assert "Jz = 0.5" in content


class TestWriteInputFiles:
    """Test input file writing."""

    def test_file_creation(self, temp_work_dir):
        """Test creation of input files."""
        sizes = [4, 6]
        # Create directory structure first
        generate_input.setup_directories(temp_work_dir, sizes)
        # Then write files
        generate_input.write_input_files(temp_work_dir, sizes, 1, 1.0)

        for size in sizes:
            stdface_path = temp_work_dir / "data" / f"N{size}" / "StdFace.def"
            assert stdface_path.exists()
            assert stdface_path.is_file()

    def test_file_content(self, temp_work_dir):
        """Test content of created files."""
        sizes = [4]
        # Create directory structure first
        generate_input.setup_directories(temp_work_dir, sizes)
        # Then write files
        generate_input.write_input_files(temp_work_dir, sizes, 1, 1.0)

        stdface_path = temp_work_dir / "data" / "N4" / "StdFace.def"
        content = stdface_path.read_text()
        assert "L = 4" in content
        assert "2S = 1" in content
        assert "Jz = 1.0" in content


class TestMain:
    """Test main function."""

    def test_successful_execution(self, temp_work_dir, capsys):
        """Test successful execution of main function."""
        test_args = [
            "prog",
            "--work-dir", str(temp_work_dir),
            "--sizes", "4,6"
        ]
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(sys, "argv", test_args)
            generate_input.main()

        # Check if files were created
        for size in [4, 6]:
            stdface_path = temp_work_dir / "data" / f"N{size}" / "StdFace.def"
            assert stdface_path.exists()

    def test_error_handling(self, temp_work_dir, capsys):
        """Test error handling in main function."""
        test_args = [
            "prog",
            "--work-dir", str(temp_work_dir),
            "--2s", "0"  # Invalid value
        ]
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(sys, "argv", test_args)
            with pytest.raises(SystemExit) as exc_info:
                generate_input.main()
            assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Error: 2S must be positive" in captured.err 
