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
