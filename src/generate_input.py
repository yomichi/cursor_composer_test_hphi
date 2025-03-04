#!/usr/bin/env python3

"""Generate input files for HPhi calculation of XXZ chain.

This script generates StdFace.def files for different system sizes
to calculate the energy gap of antiferromagnetic XXZ chain
using HPhi standard mode.
"""

import argparse
import os
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
        description="Generate input files for HPhi calculation of XXZ chain"
    )
    parser.add_argument(
        "--work-dir",
        default=".",
        help="Working directory (default: current directory)",
    )
    parser.add_argument(
        "--2s",
        type=int,
        default=1,
        help="Value of 2S (default: 1)",
    )
    parser.add_argument(
        "--delta",
        type=float,
        default=1.0,
        help="Value of Delta, Ising anisotropy (default: 1.0)",
    )
    parser.add_argument(
        "--sizes",
        default="4,6,8,10,12",
        help="Comma-separated list of system sizes (default: 4,6,8,10,12)",
    )

    args = parser.parse_args()

    # Convert sizes string to list of integers
    try:
        args.sizes = [int(s) for s in args.sizes.split(",")]
    except ValueError:
        parser.error("Invalid format for --sizes. Use comma-separated integers.")

    return args


def validate_parameters(args: argparse.Namespace) -> None:
    """Validate input parameters.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed command line arguments.

    Raises
    ------
    ValueError
        If parameters are invalid.
    """
    if args.two_s <= 0:
        raise ValueError("2S must be positive")

    if any(size <= 0 for size in args.sizes):
        raise ValueError("All sizes must be positive")


def setup_directories(work_dir: str, sizes: List[int]) -> None:
    """Set up directory structure for calculations.

    Parameters
    ----------
    work_dir : str
        Working directory path.
    sizes : List[int]
        List of system sizes.

    Raises
    ------
    OSError
        If directory creation fails.
    """
    work_path = Path(work_dir)
    data_dir = work_path / "data"

    # Create data directory if it doesn't exist
    data_dir.mkdir(parents=True, exist_ok=True)

    # Create size-specific directories
    for size in sizes:
        size_dir = data_dir / f"N{size}"
        size_dir.mkdir(exist_ok=True)


def generate_stdface(size: int, two_s: int, delta: float) -> str:
    """Generate content of StdFace.def file.

    Parameters
    ----------
    size : int
        System size.
    two_s : int
        Value of 2S.
    delta : float
        Value of Delta (Ising anisotropy).

    Returns
    -------
    str
        Content of StdFace.def file.
    """
    return f"""model = "SpinGC"
method = "CG"
lattice = "chain lattice"
L = {size}
2S = {two_s}
h = 0.0
Jx = 1.0
Jy = 1.0
Jz = {delta}
exct = 2
"""


def write_input_files(work_dir: str, sizes: List[int], two_s: int, delta: float) -> None:
    """Write StdFace.def files for each system size.

    Parameters
    ----------
    work_dir : str
        Working directory path.
    sizes : List[int]
        List of system sizes.
    two_s : int
        Value of 2S.
    delta : float
        Value of Delta (Ising anisotropy).

    Raises
    ------
    OSError
        If file writing fails.
    """
    work_path = Path(work_dir)

    for size in sizes:
        size_dir = work_path / "data" / f"N{size}"
        stdface_path = size_dir / "StdFace.def"

        content = generate_stdface(size, two_s, delta)
        
        with open(stdface_path, "w") as f:
            f.write(content)


def main():
    """Main function."""
    try:
        args = parse_args()
        validate_parameters(args)
        setup_directories(args.work_dir, args.sizes)
        write_input_files(args.work_dir, args.sizes, args.two_s, args.delta)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 