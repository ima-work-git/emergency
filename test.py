from classify_emergency import classify_text

sample = """
通報者: こ、こ、呼吸がで、できないんです
指令員: 救急車を向かわせます。場所を教えてください。
"""

category, reason = classify_text(sample)
print(category, reason)
