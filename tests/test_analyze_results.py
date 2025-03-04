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
    
    main(["--work-dir", str(temp_workdir)])
    
    assert (temp_workdir / "energy_gap.dat").exists()
    assert (temp_workdir / "energy_gap.png").exists() 
