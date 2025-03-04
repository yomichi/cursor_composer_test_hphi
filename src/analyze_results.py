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
    parser.add_argument('--work-dir', default='.',
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
    # Calculate extrapolation
    x = [1/n for n in sizes]
    fit = np.polyfit(x, gaps, 1)
    gap_infinity = np.poly1d(fit)(0)
    
    with open(output_file, 'w') as f:
        f.write("# N      E0          E1          Gap         1/N\n")
        for n, e0, e1, gap in zip(sizes, e0s, e1s, gaps):
            f.write(f"{n:3d}     {e0:.8f} {e1:.8f}  {gap:.8f}  {1/n:.8f}\n")
        f.write("#\n")
        f.write("# Linear fit: gap = ax + b\n")
        f.write(f"# a = {fit[0]:.8f}\n")
        f.write(f"# b = {fit[1]:.8f}\n")
        f.write(f"# Gap(N→∞) = {gap_infinity:.8f}\n")

def create_plot(output_file, sizes, gaps):
    """Create energy gap plot with 1/N extrapolation.

    Parameters
    ----------
    output_file : Path
        Output file path for the plot
    sizes : list
        List of system sizes
    gaps : list
        List of energy gaps
    """
    # Convert sizes to 1/N
    x = [1/n for n in sizes]
    y = gaps

    # Linear fit for extrapolation
    fit = np.polyfit(x, y, 1)
    fit_fn = np.poly1d(fit)
    
    # Create extrapolation point at 1/N = 0
    x_extrap = np.array([0])
    y_extrap = fit_fn(x_extrap)

    # Create plot
    plt.figure(figsize=(8, 6))
    
    # Plot data points
    plt.plot(x, y, 'o', label='Data')
    
    # Plot fitting line
    x_fit = np.linspace(0, max(x), 100)
    plt.plot(x_fit, fit_fn(x_fit), '--', label=f'Fit: {fit[0]:.4f}x + {fit[1]:.4f}')
    
    # Plot extrapolation point
    plt.plot(x_extrap, y_extrap, 'r*', label=f'N→∞: {y_extrap[0]:.4f}', markersize=10)
    
    plt.xlabel('1/N')
    plt.ylabel('Energy gap')
    plt.grid(True)
    plt.legend()
    
    # Adjust x-axis to show the origin
    plt.xlim(-0.01, max(x) * 1.1)
    
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
