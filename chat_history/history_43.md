### #43

#### In

ハミルトニアンは別行建ての数式にしてください。

#### Out

ハミルトニアンを別行建ての数式として見やすく修正します。

```markdown:README.md
// ... existing code ...
The scripts analyze the spin-$S$ antiferromagnetic XXZ chain:

$$
H = J\sum_{i=1}^N \left[ S_{i}^x S_{i+1}^x + S_{i}^y S_{i+1}^y + \Delta S_{i}^z S_{i+1}^z \right]
$$

where:
// ... existing code ...
スピン$S$の反強磁性XXZ鎖を解析します：

$$
H = J\sum_{i=1}^N \left[ S_{i}^x S_{i+1}^x + S_{i}^y S_{i+1}^y + \Delta S_{i}^z S_{i+1}^z \right]
$$

ここで：
// ... existing code ...
```


ハミルトニアンを`$$...$$`を使用して別行建ての数式として表示するように修正しました。これにより：

1. 数式がより見やすくなります
2. GitHubのMarkdown表示でも正しく中央揃えの別行建て数式として表示されます
3. 英語版と日本語版の両方で同じ形式で表示されます

この変更により、数式の可読性が向上し、より専門的な印象の文書となりました。
