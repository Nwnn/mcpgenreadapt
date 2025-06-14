import pandas as pd
from io import StringIO
from pathlib import Path

def load_csv(src: str | Path | StringIO) -> pd.DataFrame:
    return pd.read_csv(src)

def sample_questions(csv_src: str | Path | StringIO,
                     n: int = 1,
                     seed: int | None = None) -> pd.DataFrame:
    df = load_csv(csv_src)
    if n < 1:
        raise ValueError("n は 1 以上を指定してください。")
    if n > len(df):
        raise ValueError(f"n はデータ件数 ({len(df)}) 以下である必要があります。")
    return df.sample(n=n, random_state=seed).reset_index(drop=True)

def to_one_line_text(df: pd.DataFrame,
                     text_col: str = "article",     # ← ここを指定
                     include_id: bool = True,
                     sep: str = "\t") -> str:
    """
    DataFrame → 一行一問テキストに変換

    text_col    : 抜き出したい列名（"article" や "highlights" など）
    include_id  : True なら id と text_col を sep で連結
    sep         : 行内での区切り文字（デフォルトはタブ）
    """
    if text_col not in df.columns:
        raise KeyError(f"列 '{text_col}' が見つかりません。")

    lines = []
    for _, row in df.iterrows():
        text = str(row[text_col]).replace("\n", " ").strip()
        line  = f"{row['id']}{sep}{text}" if include_id else text
        lines.append(line)
    return "\n".join(lines)

# ----------------------- 使い方例 -----------------------
csv_path = Path(__file__).parent / "dataset" / "validation.csv"
picked = sample_questions(csv_path, n=5, seed=42)

# ① 画面に表示（id と article をタブ区切り）
print(to_one_line_text(picked, text_col="article", include_id=True))

# ② テキストファイルに保存（article だけ）
out_path = Path(__file__).parent / "sample" / "picked_articles.txt"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(to_one_line_text(picked, text_col="article", include_id=False) + "\n")
print(f"Saved to {out_path}")
