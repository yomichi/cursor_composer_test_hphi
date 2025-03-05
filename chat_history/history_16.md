### #16

#### In

```
tests/test_generate_input.py::TestWriteInputFiles::test_file_creation FAILED                                      [ 78%]
tests/test_generate_input.py::TestWriteInputFiles::test_file_content FAILED                                       [ 85%]
````

`src/generate_input.py:167: FileNotFoundError`

#### Out

エラーの原因は、`write_input_files`関数を実行する前にディレクトリ構造を作成していないためです。テストを修正します。

```python:tests/test_generate_input.py
"""Test suite for generate_input.py."""

// ... existing code ...

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

// ... rest of the code ...
```


変更点：

1. `TestWriteInputFiles`クラスの各テストメソッドで、ファイル書き込みの前に`setup_directories`を呼び出すように修正
   ```python
   # Create directory structure first
   generate_input.setup_directories(temp_work_dir, sizes)
   # Then write files
   generate_input.write_input_files(temp_work_dir, sizes, 1, 1.0)
   ```

この修正により、以下の順序で処理が行われます：

1. 一時ディレクトリの作成（pytestのフィクスチャによる）
2. データディレクトリ構造の作成（`setup_directories`による）
3. 入力ファイルの書き込み（`write_input_files`による）

これでテストが正常に実行されるはずです。再度テストを実行してみてください：

```bash
pytest tests/test_generate_input.py -v
```


