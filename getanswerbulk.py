import subprocess

# モデル名のリスト
models = ["deepseek/deepseek-r1-0528-qwen3-8b:free", "sarvamai/sarvam-m:free", "mistralai/devstral-small:free", "google/gemma-3n-e4b-it:free", "meta-llama/llama-3.3-8b-instruct:free"]  # 必要なモデル名に置き換えてください

# 各モデルに対してコマンドを実行
for model in models:
    command = ["./venv/Scripts/python", "getanswer.py", "cnndm", "-m", model]
    print(f"実行中: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)

    # 結果を出力（標準出力と標準エラーを表示）
    print("出力:")
    print(result.stdout)
    if result.stderr:
        print("エラー:")
        print(result.stderr)
