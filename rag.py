"""Recherche vectorielle + génération de réponse (RAG)."""
import os

import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer

from src.ingest import INDEX_DIR, MODEL_NAME

SYSTEM_PROMPT = (
    "Tu es un assistant du service client d'un opérateur télécom. "
    "Réponds en français, de façon claire et concise, en t'appuyant UNIQUEMENT sur les "
    "extraits de FAQ fournis. Si les extraits ne contiennent pas la réponse, dis que tu "
    "ne sais pas et invite l'utilisateur à contacter le service client. "
    "Ne donne aucune information absente des extraits."
)


class FaqRag:
    def __init__(self, seuil: float = 0.35):
        self.model = SentenceTransformer(MODEL_NAME)
        self.index = faiss.read_index(str(INDEX_DIR / "faq.index"))
        self.faq = pd.read_csv(INDEX_DIR / "faq_clean.csv")
        self.seuil = seuil  # similarité minimale pour considérer une entrée pertinente

    def retrieve(self, question: str, k: int = 3) -> list[dict]:
        q = self.model.encode([question], normalize_embeddings=True).astype("float32")
        scores, ids = self.index.search(q, k)
        resultats = []
        for score, i in zip(scores[0], ids[0]):
            ligne = self.faq.iloc[int(i)]
            resultats.append(
                {
                    "id": int(ligne["id"]),
                    "categorie": ligne["categorie"],
                    "question": ligne["question"],
                    "reponse": ligne["reponse"],
                    "score": float(score),
                }
            )
        return resultats

    def answer(self, question: str, k: int = 3) -> dict:
        sources = self.retrieve(question, k)

        if sources[0]["score"] < self.seuil:
            return {
                "reponse": "Je n'ai pas trouvé d'information fiable sur ce sujet. "
                "Merci de contacter le service client.",
                "sources": sources,
                "mode": "hors_perimetre",
            }

        if not os.getenv("ANTHROPIC_API_KEY"):
            return {"reponse": sources[0]["reponse"], "sources": sources, "mode": "retrieval"}

        import anthropic

        contexte = "\n\n".join(
            f"[{s['id']}] Q : {s['question']}\nR : {s['reponse']}" for s in sources
        )
        client = anthropic.Anthropic()
        message = client.messages.create(
            model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5"),
            max_tokens=400,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"Extraits de FAQ :\n{contexte}\n\nQuestion : {question}",
                }
            ],
        )
        return {"reponse": message.content[0].text, "sources": sources, "mode": "rag"}
