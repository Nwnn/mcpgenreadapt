from pathlib import Path


def create_summary_prompt(input_file: Path,
                          output_file: Path,
                          instruction: str = "Please provide a short, concise summary of all the text in the following sections:") -> None:
    """
    picked_articles.txt の各行を読み込み、番号付きで要約タスクを並べたプロンプトを生成して prompt.txt に保存する

    input_file  : 読み込むテキストファイルのパス
    output_file : プロンプトを保存するファイルのパス
    instruction : LLM に与える要約指示文
    """
    # テキストを行ごとに取得し空行を除去
    lines = [line.strip() for line in input_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    # 番号付きプロンプトを組み立て
    sections = []
    for idx, text in enumerate(lines, start=1):
        sections.append(f"{idx}.\n{text}")
    body = "\n\n".join(sections)
    prompt = f"{instruction}\n\n{body}\n"
    # ファイルに書き出し
    output_file.write_text(prompt, encoding="utf-8")
    print(f"Prompt saved to {output_file}")


if __name__ == "__main__":
    base_dir = Path(__file__).parent
    input_path = base_dir / "sample" / "picked_articles.txt"
    output_path = base_dir / "prompt" / "prompt.txt"
    create_summary_prompt(input_path, output_path)