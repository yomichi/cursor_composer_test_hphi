### #27

#### In

HPhiのマニュアルによると、 `method=CG` のときの `zvo_energy.dat` のファイル形式は次のとおりです。
```
State 0
  Energy  -7.1043675920
  Doublon  0.4164356536
  Sz  0.0000000000

State 1
:
```

これを参考に、テストの仕様書を修正してください。

#### Out

テスト仕様書を修正させていただきます。`zvo_energy.dat`のファイル形式に関する部分を更新する必要があります。

````markdown:references/tests/analyze_results.py.md
// ... existing code ...
### サンプルデータ
```
# zvo_energy.dat の例（method=CG）
State 0
  Energy  -7.1043675920
  Doublon  0.4164356536
  Sz  0.0000000000

State 1
  Energy  -6.9876543210
  Doublon  0.3987654321
  Sz  0.0000000000

# energy_gap.dat の期待される形式
# N      E0          E1          Gap
  4     -7.10436759 -6.98765432  0.11671327
  6     -12.1234568 -11.9876543  0.13580246
  8     -16.1234568 -15.9876543  0.13580246
``` 
// ... existing code ...
````


また、エネルギー値の読み込みに関するテストケースも修正する必要があります。

````markdown:references/tests/analyze_results.py.md
// ... existing code ...
### エネルギー値の読み込み（`test_read_energies`）
- 正常系
  - エネルギーファイルの読み込み
  - `State 0`と`State 1`のブロックからのエネルギー値抽出
  - `Energy`行からの数値抽出と型変換
  - 数値の型と精度の確認（10桁の浮動小数点数）
- 異常系
  - ファイルが存在しない場合
  - ファイルフォーマットが不正な場合
    - `State`ブロックが見つからない
    - `Energy`行が見つからない
    - エネルギー値が数値として解釈できない
  - エネルギー値の順序が不正な場合（E₁ < E₀）
  - 必要な状態数（State 0とState 1）が見つからない場合
// ... existing code ...
````


修正のポイントについて説明させていただきます：

1. **ファイル形式の更新**：
   - `zvo_energy.dat`のサンプルを、HPhiの`method=CG`での実際の出力形式に合わせました
   - 各状態（State）がブロック形式で記述され、その中にエネルギーや他の物理量が含まれる形式を反映

2. **エネルギー値の読み込みテストの詳細化**：
   - ファイル解析の手順をより具体的に記述
   - `State`ブロックの検出と解析
   - `Energy`行からの値の抽出
   - 浮動小数点数の精度（10桁）の確認
   - エラーケースの具体化

これらの変更により、テスト仕様がHPhiの実際の出力形式により適合したものになりました。テストケースは、ファイルの構造的な解析とエネルギー値の抽出の両方をカバーするように設計されています。


