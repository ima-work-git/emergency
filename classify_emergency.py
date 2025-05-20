import os
import re
import csv
import unicodedata
from difflib import SequenceMatcher

PRIORITY_ORDER = ["life_threatening", "serious", "minor"]

# カテゴリごとのキーワード（表記ゆれを含む）
CATEGORY_KEYWORDS = {
    "life_threatening": [
        "意識がない", "意識なし", "意識がありません", "反応がない", "ぐったり",
        "呼吸がない", "呼吸なし", "息をしていない", "息してない",
        "心臓", "胸が痛い",
        "大量の出血", "大量出血", "血が止まらない",
        "倒れて動かない", "倒れている", "倒れて意識がない",
    ],
    "serious": [
        "呼吸困難", "息苦しい", "息がしづらい", "ぜーぜー", "呼吸が辛い", "呼吸ができない",
        "激しい痛み", "激痛", "耐えられない痛み",
        "火災", "火事", "煙が出ている",
        "交通事故", "事故", "衝突", "ぶつかった",
    ],
    "minor": [
        "軽いけが", "軽傷", "擦り傷", "切り傷",
        "発熱", "熱がある", "高熱", "微熱",
        "体調不良", "気分が悪い", "具合が悪い", "だるい",
    ],
}

def normalize_text(text: str) -> str:
    """簡易的な正規化を行い表記ゆれを吸収する。"""
    text = unicodedata.normalize("NFKC", text)
    text = text.lower()
    text = re.sub(r"^(通報者|指令員|通信指令員)[:：]\s*", "", text)
    text = re.sub(r"[、。,．.：:・\s]", "", text)
    text = re.sub(r"(.)\1{2,}", r"\1", text)  # 連続文字（吃音など）を圧縮
    return text

def keyword_in_line(line: str, keyword: str) -> bool:
    """行内にキーワードが存在するかをあいまいに判定する。"""
    if keyword in line:
        return True
    ratio = SequenceMatcher(None, line, keyword).ratio()
    return ratio >= 0.7

def classify_text(text: str):
    """キーワード検索により緊急度カテゴリと理由を返す。"""
    lines = [normalize_text(l) for l in text.splitlines()]
    for category in PRIORITY_ORDER:
        for kw in CATEGORY_KEYWORDS[category]:
            kw_norm = normalize_text(kw)
            for line in lines:
                if keyword_in_line(line, kw_norm):
                    return category, kw
    return "unknown", "なし"

def process_directory(path: str, output_csv: str):
    """ディレクトリ内のテキストファイルを分類し CSV に出力する。"""
    rows = []
    for filename in os.listdir(path):
        if not filename.endswith('.txt'):
            continue
        with open(os.path.join(path, filename), 'r', encoding='utf-8') as f:
            content = f.read()
        category, reason = classify_text(content)
        rows.append({'file': filename, 'category': category, 'reason': reason})
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['file', 'category', 'reason'])
        writer.writeheader()
        writer.writerows(rows)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Classify emergency call transcripts.')
    parser.add_argument('directory', help='Directory containing call text files')
    parser.add_argument('--output', default='result.csv', help='Output CSV file')
    args = parser.parse_args()

    process_directory(args.directory, args.output)
