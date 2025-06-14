from pathlib import Path
import pandas as pd

def create_math_prompt(input_csv: Path,
                       output_file: Path,
                       instruction: str = "Please solve the following math problems in order. Please provide the steps and answer for each problem :") -> None:
    """
    CSVの'question'列から問題文を読み込み、番号付きで並べたプロンプトを生成し prompt.txt に保存する

    input_csv   : 読み込むCSVファイルのパス（question列が必要）
    output_file : 出力するプロンプトファイルのパス
    instruction : LLMに与える全体指示文
    """
    # CSV読み込み
    df = pd.read_csv(input_csv)
    if 'question' not in df.columns:
        raise KeyError("CSVに 'question' 列が見つかりません。")

    # 各行を番号付きテキストに変換
    sections = []
    for idx, q in enumerate(df['question'].fillna(""), start=1):
        text = str(q).strip().replace("\n", " ")
        sections.append(f"{idx}.\n{text}")

    # プロンプト組み立て
    body = "\n\n".join(sections)
    prompt = f"{instruction}\n\n{body}\n\nAnswer："

    # ファイル書き出し
    output_file.write_text(prompt, encoding="utf-8")
    print(f"Prompt saved to {output_file}")


if __name__ == "__main__":
    base_dir = Path(__file__).parent
    input_path = base_dir / "sample" / "output.csv"
    output_path = base_dir / "prompt" / "prompt.txt"
    create_math_prompt(input_path, output_path)
