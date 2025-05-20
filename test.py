import os
import subprocess

# 簡単な動作確認用テスト

def main():
    os.makedirs("sample_calls", exist_ok=True)
    with open("sample_calls/call1.txt", "w", encoding="utf-8") as f:
        f.write("通報者: 呼吸なしで倒れています\n")
    with open("sample_calls/call2.txt", "w", encoding="utf-8") as f:
        f.write("通報者: 胸が痛いです\n")

    subprocess.run(["python", "classify_emergency.py", "sample_calls", "--output", "out.csv"], check=True)

    with open("out.csv", "r", encoding="utf-8") as f:
        print(f.read())

if __name__ == "__main__":
    main()
