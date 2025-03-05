### #32

コマンドラインオプションの仕様を勝手に変えてきたので戻させる

#### In

コマンドラインオプションに関する仕様に従ってください。作業ディレクトリの指定は、位置引数ではなくてオプション `--work-dir` にしてください。

#### Out

はい、コマンドラインオプションの仕様を修正します。`--work-dir`をオプション引数として実装し直します。

```python:src/analyze_results.py
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
```


次に、テストコードも修正します：

```python:tests/test_analyze_results.py
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

// ... existing code ...

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
```


修正のポイントについて説明させていただきます：

1. **`parse_args`関数の変更**:
   - 位置引数（`work_dir`）をオプション引数（`--work-dir`）に変更
   - `nargs='?'`を削除し、通常のオプション引数として実装

2. **テストケースの更新**:
   - `test_parse_args`のテストケースはそのまま（既に`--work-dir`を使用していたため）
   - `test_main`のコマンドライン引数を`["--work-dir", str(temp_workdir)]`に修正

これにより、以下のような使用方法が可能になります：

```bash
# デフォルトの作業ディレクトリ（カレントディレクトリ）を使用
python src/analyze_results.py

# 特定の作業ディレクトリを指定
python src/analyze_results.py --work-dir /path/to/work
```

この修正により、コマンドラインオプションの仕様に準拠した実装になりました。


