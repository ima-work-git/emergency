import os
import re
import csv

# ----------------------------------------------------------------------
# 簡易キーワード辞書
#   本来は Appendix A〜D を用いた詳細判定が必要だが、ここでは代表的な語のみを使用
# ----------------------------------------------------------------------
CPA_WORDS = [
    "呼吸なし",
    "脈なし",
    "意識なし",
    "冷たくなっている",
    "水没",
    "首をつった",
    "首を絞めた",
    "喉が詰まった",
]

# 高危険症候（Appendix B）
HIGH_RISK = [
    "呼吸困難",
    "動悸",
    "意識障害",
    "失神",
    "けいれん",
    "頭痛",
    "胸痛",
    "胸が痛い",
    "背部痛",
    "腰部痛",
]

SERIOUS = ["大量出血", "骨折", "火災", "交通事故"]
MINOR = ["発熱", "めまい", "軽いけが", "擦り傷"]

CODE_KEYWORDS = {
    "R1": CPA_WORDS,
    "R2": SERIOUS,
    "Y1": HIGH_RISK,
    "Y2": MINOR,
}

# ----------------------------------------------------------------------
# 正規化処理
#   ・発話者ラベル (例: "指令員:") を除去
#   ・同一文字の連続を 2 文字に圧縮
# ----------------------------------------------------------------------
def normalize_text(text: str) -> str:
    text = re.sub(r"^[^:]{1,4}:", "", text, flags=re.MULTILINE)
    text = re.sub(r"(.)\1{2,}", r"\1\1", text)
    return text

# ----------------------------------------------------------------------
# 緊急度判定
# ----------------------------------------------------------------------
def classify_text(text: str) -> tuple[str, str]:
    """テキストから緊急度コードと理由を返す"""
    normalized = normalize_text(text)
    for code, words in CODE_KEYWORDS.items():
        for w in words:
            if w in normalized:
                return code, f"キーワード『{w}』を検出"
    return "R3", "該当キーワードなし"

# ----------------------------------------------------------------------
# ディレクトリ処理
# ----------------------------------------------------------------------
def process_directory(path: str, output_csv: str) -> None:
    rows = []
    for filename in os.listdir(path):
        if not filename.endswith(".txt"):
            continue
        with open(os.path.join(path, filename), "r", encoding="utf-8") as f:
            content = f.read()
        code, reason = classify_text(content)
        rows.append({"file": filename, "code": code, "reason": reason})

    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["file", "code", "reason"])
        writer.writeheader()
        writer.writerows(rows)

# ----------------------------------------------------------------------
# メイン処理
# ----------------------------------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="通報テキストを緊急度分類する")
    parser.add_argument("directory", help="テキストファイルをまとめたディレクトリ")
    parser.add_argument("--output", default="result.csv", help="結果CSV")
    args = parser.parse_args()

    process_directory(args.directory, args.output)
