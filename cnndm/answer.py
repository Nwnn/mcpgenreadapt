from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os
from cnndm.prompt import build_prompt  # 追加

load_dotenv()  # .envファイルを読み込む

# ---------- 設定 ----------
TEXT_PATH = "./cnndm/picked_articles.txt"          # 一行一問テキスト
MODEL_NAME = "deepseek/deepseek-r1-0528-qwen3-8b:free"
BASE_URL   = "https://openrouter.ai/api/v1"
API_KEY = os.getenv("OPENROUTER_API_KEY")         # ★ご自身のキーに置き換えてください
SITE_URL   = "<YOUR_SITE_URL>"              # Optional
SITE_TITLE = "<YOUR_SITE_NAME>"             # Optional
# --------------------------

def summarize_text(text: str) -> str:
    """与えられた文字列を要約 (OpenRouter 経由)"""
    client = OpenAI(
        base_url=BASE_URL,
        api_key=API_KEY,
    )

    prompt = build_prompt(text)  # プロンプト生成を外部化

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        # extra_headers={
        #     "HTTP-Referer": SITE_URL,
        #     "X-Title": SITE_TITLE,
        # },
        # extra_body={},  # 必要なら追加パラメータをここで
        messages=prompt,
        temperature=0.3,        # 要約なので低めに
        max_tokens=1024         # 必要に応じて増減
    )
    return completion.choices[0].message.content.strip()

def main():
    # ❶ テキスト読み込み
    text = Path(TEXT_PATH).read_text(encoding="utf-8").strip()

    # ❷ 要約
    summary = summarize_text(text)

    # ❸ 出力
    print("=== summary ===")
    print(summary)

    safe_model = MODEL_NAME.replace('/', '_').replace(':', '_')
    output_filename = f"./cnndm/summary_{safe_model}.txt"
    output_path = Path(output_filename)
    output_path.write_text(summary, encoding="utf-8")
    print(f"Saved summary to {output_path}")

if __name__ == "__main__":
    main()
    print(summary)

    safe_model = MODEL_NAME.replace('/', '_').replace(':', '_')
    output_filename = f"./cnndm/summary_{safe_model}.txt"
    output_path = Path(output_filename)
    output_path.write_text(summary, encoding="utf-8")
    print(f"Saved summary to {output_path}")

if __name__ == "__main__":
    main()
