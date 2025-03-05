### #38

#### In

```
================================================ short test summary info ================================================
FAILED tests/test_analyze_results.py::test_create_plot - NameError: name 'analyze_results' is not defined
=
```

#### Out

あぁ、申し訳ありません。テストコードでモジュールのインポート方法を修正する必要があります。

```python:tests/test_analyze_results.py
import pytest
import os
import tempfile
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import analyze_results
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

@pytest.fixture(autouse=True)
def setup_and_cleanup():
    # Setup: ensure args is initialized
    if not hasattr(analyze_results, 'args'):
        analyze_results.args = parse_args([])
    yield
    # Cleanup: reset args
    if hasattr(analyze_results, 'args'):
        delattr(analyze_results, 'args')

def test_parse_args(temp_workdir):
    # Test default values
    args = parse_args([])
    assert args.work_dir == "."
    assert args.formats == ["pdf"]

    # Test custom work directory
    args = parse_args(["--work-dir", str(temp_workdir)])
    assert args.work_dir == str(temp_workdir)
    assert args.formats == ["pdf"]

    # Test format option
    args = parse_args(["--format", "png"])
    assert args.formats == ["png"]

    args = parse_args(["--format", "pdf,png"])
    assert args.formats == ["pdf", "png"]

    # Test invalid format
    with pytest.raises(SystemExit):
        parse_args(["--format", "jpg"])

    # Test duplicate format
    with pytest.raises(SystemExit):
        parse_args(["--format", "pdf,pdf"])

    # Test non-existent directory
    with pytest.raises(SystemExit):
        parse_args(["--work-dir", "/non/existent/path"])

// ... existing code ...

def test_create_plot(temp_workdir):
    sizes = [4, 6, 8]
    gaps = [0.11671327, 0.13580246, 0.13580246]
    plot_file = temp_workdir / "energy_gap"

    # Test PDF output (default)
    analyze_results.args = parse_args(["--format", "pdf"])
    create_plot(plot_file, sizes, gaps)
    assert (plot_file.with_suffix('.pdf')).exists()
    
    # Test PNG output
    analyze_results.args = parse_args(["--format", "png"])
    create_plot(plot_file, sizes, gaps)
    assert (plot_file.with_suffix('.png')).exists()
    
    # Test multiple formats
    analyze_results.args = parse_args(["--format", "pdf,png"])
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

1. **モジュールのインポート修正**:
   - `import analyze_results`を追加して、モジュール全体をインポート
   - これにより`analyze_results.args`にアクセス可能に

2. **フィクスチャの追加**:
   - `setup_and_cleanup`フィクスチャを追加
   - テスト前に`args`を初期化
   - テスト後に`args`をクリーンアップ
   - `autouse=True`で全テストに自動適用

3. **テストケースの改善**:
   - `analyze_results.args`の設定方法を統一
   - 各テストケースでの適切な初期化と後処理

これらの修正により、以下の問題が解決されます：
- `analyze_results`モジュールが見つからないエラー
- `args`変数の未定義エラー
- テスト間での状態の干渉

テストを再実行すると、すべてのテストがパスするはずです。


