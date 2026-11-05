"""Add the article texts (first 1,500 characters) to data/annotation_pairs.csv, from the CC-News copy
already downloaded by check_copies.py.  Writes data/annotation_pairs_texts.csv.  No GPU, ~2 minutes.

  python export_pair_texts.py
"""
from pathlib import Path

import pandas as pd
from datasets import load_dataset

HERE = Path(__file__).resolve().parent


def main():
    pairs = pd.read_csv(HERE / "data" / "annotation_pairs.csv")
    urls = set(pairs.url_a) | set(pairs.url_b)
    for name in ("vblagoje/cc_news", "cc_news"):
        try:
            ds = load_dataset(name, split="train")
            break
        except Exception as e:  # noqa: BLE001
            print(f"{name}: {e.__class__.__name__}")
    df = ds.select_columns(["url", "text"]).to_pandas()   # plain pandas: no worker processes on Windows
    df = df[df.url.isin(urls)].drop_duplicates("url")
    text = dict(zip(df.url, df.text.str[:1500]))
    pairs["text_a"] = pairs.url_a.map(text)
    pairs["text_b"] = pairs.url_b.map(text)
    pairs.to_csv(HERE / "data" / "annotation_pairs_texts.csv", index=False)
    print(f"{pairs.text_a.notna().sum()} + {pairs.text_b.notna().sum()} texts found for {len(pairs)} pairs")


if __name__ == "__main__":
    main()
