import json
import random
import csv
from pathlib import Path

# 設定
input_json = Path(__file__).parent / "dataset" / 'dev-v2.0.json'   # 入力SQuADファイル
output_csv = Path(__file__).parent / "sample" / 'sample_output.csv' # 出力CSVファイル
sample_size = 5                        # サンプル数
seed = None                            # シード（再現性用）

def extract_qas(json_path):
    """SQuAD形式のjsonから全QAペアを抽出"""
    with open(json_path, 'r', encoding='utf-8') as f:
        squad = json.load(f)
    qas_list = []
    for article in squad['data']:
        for para in article['paragraphs']:
            context = para['context']
            for qa in para['qas']:
                qas_list.append({
                    'id': qa['id'],
                    'question': qa['question'],
                    'context': context,
                    'is_impossible': qa.get('is_impossible', False),
                    'answers': json.dumps(qa.get('answers', []), ensure_ascii=False)
                })
    return qas_list

def sample_and_save(json_path, csv_path, sample_size=5, seed=None):
    qas_list = extract_qas(json_path)
    if sample_size > len(qas_list):
        raise ValueError(f"sample_size({sample_size}) > total QAs({len(qas_list)})")
    if seed is not None:
        random.seed(seed)
    sampled = random.sample(qas_list, sample_size)
    fieldnames = ['id', 'question', 'context', 'is_impossible', 'answers']
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sampled)

if __name__ == '__main__':
    sample_and_save(input_json, output_csv, sample_size, seed)