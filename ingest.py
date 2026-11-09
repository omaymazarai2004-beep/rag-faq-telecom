"""Construction de l'index vectoriel à partir de la FAQ."""
from pathlib import Path

import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
ROOT = Path(__file__).resolve().parent.parent
FAQ_PATH = ROOT / "data" / "faq.csv"
INDEX_DIR = ROOT / "index"


def load_faq(path: Path = FAQ_PATH) -> pd.DataFrame:
    """Charge la FAQ, supprime les lignes incomplètes et prépare le texte à vectoriser."""
    df = pd.read_csv(path).dropna(subset=["question", "reponse"]).reset_index(drop=True)
    df["texte"] = df["question"].str.strip() + " " + df["reponse"].str.strip()
    return df


def build_index(faq_path: Path = FAQ_PATH, out_dir: Path = INDEX_DIR) -> None:
    out_dir.mkdir(exist_ok=True)
    df = load_faq(faq_path)

    model = SentenceTransformer(MODEL_NAME)
    # Vecteurs normalisés : le produit scalaire équivaut alors à la similarité cosinus.
    emb = model.encode(df["texte"].tolist(), normalize_embeddings=True, show_progress_bar=True)
    emb = emb.astype("float32")

    index = faiss.IndexFlatIP(emb.shape[1])
    index.add(emb)

    faiss.write_index(index, str(out_dir / "faq.index"))
    df.to_csv(out_dir / "faq_clean.csv", index=False)
    print(f"Index construit : {index.ntotal} entrées, dimension {emb.shape[1]}")


if __name__ == "__main__":
    build_index()
