"""Write the labels for the public repository WITHOUT article text (the texts belong to the outlets;
anyone can rebuild them from CC-News with export_pair_texts.py / export_independent_pairs.py).

  python make_release_labels.py

  data/labels_dependence.csv          300 pairs of Section 3: URLs, titles, AI-drafted dependence label
  data/labels_iaa.csv                 100 blind pairs: label of author 1 (Metales), author 2
                                      (Grabenheinrich) and the AI draft
  data/labels_independent_check.csv   40 audited comparison pairs of Section 6
  data/labels_indep_set.csv           250 held-out same-event pairs of Section 6, labels of both authors
The xlsx and text files they come from stay local (.gitignore).
"""
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
D = HERE / "data"


def main():
    a = pd.read_csv(D / "annotation_pairs_labelled.csv")
    if "miriam_label" in a and a.miriam_label.notna().any():
        a["label"] = a.miriam_label.where(a.miriam_label.notna() & (a.miriam_label != ""), a.label)
    a = a[["pair", "kind_by_detector", "similarity", "domain_a", "url_a", "title_a", "domain_b", "url_b", "title_b",
           "label", "confidence", "reason"]]
    a.to_csv(D / "labels_dependence.csv", index=False)

    key = pd.read_csv(D / "iaa_key.csv").rename(columns={"label": "label_ai_draft"})
    who = {}
    for name, col in (("kader", "author1"), ("miriam", "author2")):
        s = pd.read_excel(D / f"iaa_{name}.xlsx", sheet_name="Pairs")
        who[col] = s.set_index("item")
    i = key.set_index("item")
    i["url_a"], i["url_b"] = who["author1"].url_a, who["author1"].url_b
    for col, s in who.items():
        i[f"label_{col}"] = s.your_label.astype(str).str.strip()
        i[f"comment_{col}"] = s.your_comment
    i.reset_index()[["item", "pair", "url_a", "url_b", "label_author1", "label_author2", "label_ai_draft",
                     "comment_author1", "comment_author2"]].to_csv(D / "labels_iaa.csv", index=False)

    c = pd.read_excel(D / "independent_check_labelled.xlsx")
    c.drop(columns=[x for x in c if x.startswith("text_")]).to_csv(D / "labels_independent_check.csv", index=False)

    k = pd.read_csv(D / "indep_set_key.csv").set_index("item")
    for who in ("author1", "author2"):
        k[f"label_{who}"] = pd.read_excel(D / f"indep_set_{who}.xlsx", sheet_name="Pairs").set_index("item").label
    k.reset_index().to_csv(D / "labels_indep_set.csv", index=False)

    for f in ("labels_dependence.csv", "labels_iaa.csv", "labels_independent_check.csv", "labels_indep_set.csv"):
        t = pd.read_csv(D / f)
        assert not any(col.startswith("text") for col in t), f
        print(f"data/{f}: {len(t)} rows, columns {list(t.columns)}")


if __name__ == "__main__":
    main()
