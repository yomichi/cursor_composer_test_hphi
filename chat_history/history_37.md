### #37

#### In

`python3 -m pytest tests/test_analyze_results.py` が失敗しました

```
================================================ short test summary info ================================================
FAILED tests/test_analyze_results.py::test_create_plot - ValueError: Key savefig.format: Could not convert ['pdf'] to str
FAILED tests/test_analyze_results.py::test_main - ValueError: Key savefig.format: Could not convert ['pdf'] to str
```

#### Out

はい、`matplotlib`の`rcParams`の使用方法に問題があるようです。`savefig.format`は文字列のリストではなく、単一の文字列を期待します。修正します。

```python:src/analyze_results.py
def create_plot(output_file, sizes, gaps):
    """Create energy gap plot with 1/N extrapolation.

    Parameters
    ----------
    output_file : Path
        Output file path for the plot (without extension)
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
    
    # Save plot in specified formats
    for fmt in args.formats:
        plt.savefig(f"{output_file}.{fmt}")
    plt.close()

def main(argv=None):
    """Main function to analyze HPhi results.

    Parameters
    ----------
    argv : list, optional
        Command line arguments, by default None
    """
    global args
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
    create_plot(work_dir / "energy_gap", sizes, gaps)
```




次に、テストコードも修正します：

```python:tests/test_analyze_results.py
def test_create_plot(temp_workdir):
    sizes = [4, 6, 8]
    gaps = [0.11671327, 0.13580246, 0.13580246]
    
    # Test PDF output (default)
    plot_file = temp_workdir / "energy_gap"
    analyze_results.args = analyze_results.parse_args(["--format", "pdf"])
    create_plot(plot_file, sizes, gaps)
    assert (plot_file.with_suffix('.pdf')).exists()
    
    # Test PNG output
    analyze_results.args = analyze_results.parse_args(["--format", "png"])
    create_plot(plot_file, sizes, gaps)
    assert (plot_file.with_suffix('.png')).exists()
    
    # Test multiple formats
    analyze_results.args = analyze_results.parse_args(["--format", "pdf,png"])
    create_plot(plot_file, sizes, gaps)
    assert (plot_file.with_suffix('.pdf')).exists()
    assert (plot_file.with_suffix('.png')).exists()

def test_main(temp_workdir, sample_energy_data):
    # Create test data structure
    for n in [4, 6, 8]:
        result_dir = temp_workdir / f"results/raw/N{n}"
        result_dir.mkdir(parents=True)
        energy_file = result_dir / "zvo_energy.dat"
        energy_file.parent.mkdir(parents=True, exist_ok=True)
        energy_file.write_text(sample_energy_data)
    
    # Test default format (PDF)
    main(["--work-dir", str(temp_workdir)])
    assert (temp_workdir / "energy_gap.dat").exists()
    assert (temp_workdir / "energy_gap.pdf").exists()
    
    # Test multiple formats
    main(["--work-dir", str(temp_workdir), "--format", "pdf,png"])
    assert (temp_workdir / "energy_gap.pdf").exists()
    assert (temp_workdir / "energy_gap.png").exists()
```




主な修正点について説明させていただきます：

1. **プロット形式の処理変更**:
   - `plt.rcParams['savefig.format']`の使用を廃止
   - `args.formats`を直接使用して各形式でファイルを保存

2. **グローバル変数の追加**:
   - `args`をグローバル変数として定義
   - `create_plot`関数で`args.formats`にアクセス可能に

3. **テストケースの更新**:
   - `test_create_plot`で`analyze_results.args`を直接設定
   - 各テストケースで適切なコマンドライン引数を使用

これらの修正により、以下の問題が解決されます：
- `savefig.format`に関するエラー
- 複数フォーマットでの出力の正しい処理
- テストケースの適切な実行

テストを再実行すると、すべてのテストがパスするはずです。


