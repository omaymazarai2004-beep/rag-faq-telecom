"""Évaluation de la récupération : Hit@k et MRR."""
from pathlib import Path

import pandas as pd

from src.rag import FaqRag

ROOT = Path(__file__).resolve().parent.parent
EVAL_PATH = ROOT / "eval" / "questions.csv"


def evaluer(k_max: int = 5) -> dict:
    rag = FaqRag()
    df = pd.read_csv(EVAL_PATH)

    rangs = []
    for _, ligne in df.iterrows():
        ids = [r["id"] for r in rag.retrieve(ligne["question"], k=k_max)]
        attendu = int(ligne["id_attendu"])
        rangs.append(ids.index(attendu) + 1 if attendu in ids else None)

    n = len(rangs)
    resultats = {f"Hit@{k}": sum(r is not None and r <= k for r in rangs) / n for k in (1, 3, 5)}
    resultats["MRR"] = sum(1 / r for r in rangs if r) / n

    echecs = df[[r is None or r > 1 for r in rangs]]
    return {"metriques": resultats, "echecs_top1": echecs}


if __name__ == "__main__":
    res = evaluer()
    for nom, valeur in res["metriques"].items():
        print(f"{nom} : {valeur:.3f}")
    if not res["echecs_top1"].empty:
        print("\nQuestions non classées en 1re position :")
        print(res["echecs_top1"].to_string(index=False))
