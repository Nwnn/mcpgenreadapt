from pathlib import Path
import pandas as pd

def create_squad_prompt(input_csv: Path,
                        output_file: Path,
                        instruction: str = "以下の文章を読んで、各質問に回答してください。回答には根拠となる文章の一部を引用してください。") -> None:
    """
    SQuAD形式のCSVから 'context' と 'question' 列を読み込み、
    番号付きで文章と質問を並べたプロンプトを生成し prompt.txt に保存する

    input_csv   : 読み込むCSVファイルのパス（'context','question' 列が必要）
    output_file : 出力するプロンプトファイルのパス
    instruction : LLMに与える全体指示文
    """
    # CSV読み込み
    df = pd.read_csv(input_csv)
    missing = [col for col in ('context', 'question') if col not in df.columns]
    if missing:
        raise KeyError(f"CSVに以下の列が見つかりません: {missing}")

    # 各行を番号付きで組み立て
    sections = []
    for idx, row in df.iterrows():
        ctx = str(row['context']).replace("\n", " ").strip()
        qst = str(row['question']).replace("\n", " ").strip()
        sections.append(f"{idx+1}.\n文章: {ctx}\n質問: {qst}")

    # 本文を結合しプロンプト作成
    body = "\n\n".join(sections)
    prompt = f"{instruction}\n\n{body}\n\n回答："

    # ファイル書き出し
    output_file.write_text(prompt, encoding="utf-8")
    print(f"Prompt saved to {output_file}")


if __name__ == "__main__":
    base_dir = Path(__file__).parent
    input_path = base_dir / "sample" / "sample_output.csv"
    output_path = base_dir / "prompt" / "prompt.txt"
    create_squad_prompt(input_path, output_path)
