import argparse
from pathlib import Path
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ---------- 定数 ----------
BASE_URL = "https://openrouter.ai/api/v1"
# デフォルトモデルは deepseek
DEFAULT_MODEL = "deepseek/deepseek-r1-0528-qwen3-8b:free"
API_KEY = os.getenv("OPENROUTER_API_KEY")
# 出力先ディレクトリ
OUTPUT_DIR = Path("./answers")
# ------------------------


def summarize_text(prompt: str, model: str) -> str:
    """
    与えられたプロンプトを LLM 経由で要約／回答取得
    model: OpenRouter 上のモデル名
    """
    client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            # {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",   "content": prompt},
        ],
        temperature=0.3,
        max_tokens=4096,
    )
    return completion.choices[0].message.content.strip()


def main():
    parser = argparse.ArgumentParser(
        description="各データセットのプロンプトを読み込み、指定モデルでLLMに投げて回答を取得する"
    )
    parser.add_argument(
        "dataset",
        choices=["cnndm", "gsm", "squad"],
        help="対象データセット名を指定 (cnndm, gsm, squad)"
    )
    parser.add_argument(
        "--model", "-m",
        default=DEFAULT_MODEL,
        help=f"使用するモデル名 (デフォルト: {DEFAULT_MODEL})"
    )
    args = parser.parse_args()

    base_dir = Path(__file__).parent
    data_dir = base_dir / args.dataset
    prompt_path = data_dir / "prompt" / "prompt.txt"
    if not prompt_path.exists():
        print(f"Error: プロンプトファイルが見つかりません: {prompt_path}")
        return

    # プロンプト読み込み
    prompt = prompt_path.read_text(encoding="utf-8").strip()

    # LLM 実行
    print(f"=== Running LLM for dataset: {args.dataset}, model: {args.model} ===")
    response = summarize_text(prompt, args.model)
    print("=== Response ===")
    print(response)

    # 出力ディレクトリ作成
    OUTPUT_DIR.mkdir(exist_ok=True)
    # ファイル名: answers/{dataset}_{modelをsafe化}.txt
    safe_model = args.model.replace('/', '_').replace(':', '_')
    out_filename = f"{args.dataset}_{safe_model}.txt"
    out_path = OUTPUT_DIR / out_filename
    out_path.write_text(response, encoding="utf-8")
    print(f"Saved answer to {out_path}")

if __name__ == "__main__":
    main()
