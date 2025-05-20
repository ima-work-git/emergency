# Emergency Call Classification

このリポジトリには、簡易的な緊急度判定スクリプトが含まれています。会話特有の表記ゆれを吸収するため、キーワードは同義語を拡充し、簡易正規化処理を施しています。なお、参照 PDF を取得できない環境のため、カテゴリや判定基準は暫定的なものです。

## Usage

1. Prepare a directory containing text files. Each file represents one emergency call conversation. Lines alternate between the caller and the dispatcher.
2. Run the classification script:

```bash
python classify_emergency.py /path/to/call_directory --output result.csv
```

実行すると、各ファイル名と判定された緊急度、マッチしたキーワードを記載した CSV が生成されます。

## 注意

カテゴリやキーワードは暫定的なものです。正式な判定基準は消防庁 PDF の該当ページを参照してください。
