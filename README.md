# Chatbot RAG sur une base de FAQ télécom

Assistant de questions-réponses en français pour une FAQ d'opérateur télécom. Le système retrouve les entrées de FAQ les plus proches de la question (embeddings multilingues + recherche vectorielle), puis génère une réponse fondée uniquement sur ces entrées, avec citation des sources.

> Les données fournies dans `data/faq.csv` sont **fictives** (inspirées des thèmes courants d'une FAQ télécom : offres, facturation, fibre, dépannage). Remplace-les par une FAQ publique réelle si tu veux un projet plus riche.

## Architecture

```
FAQ (CSV) -> nettoyage -> embeddings (sentence-transformers) -> index FAISS
Question  -> embedding -> top-k entrées -> prompt (contexte + question) -> LLM -> réponse + sources
```

- **Embeddings** : `paraphrase-multilingual-MiniLM-L12-v2` (français, arabe, anglais)
- **Index** : FAISS (produit scalaire sur vecteurs normalisés = similarité cosinus)
- **Génération** : API Anthropic (optionnelle). Sans clé API, le mode « retrieval seul » renvoie la meilleure entrée de FAQ.
- **Interface** : Streamlit
- **Évaluation** : Hit@k et MRR sur un jeu de questions reformulées

## Installation

```bash
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

## Utilisation

```bash
python -m src.ingest             # construit l'index dans index/
python -m src.evaluate           # calcule Hit@k et MRR
streamlit run app.py             # lance l'interface
```

Pour activer la génération : `export ANTHROPIC_API_KEY=...` (Windows : `set ANTHROPIC_API_KEY=...`).

## Structure

```
data/faq.csv            base de FAQ (id, categorie, question, reponse)
eval/questions.csv      questions de test avec l'id attendu
src/ingest.py           chargement, embeddings, index
src/rag.py              recherche + génération
src/evaluate.py         métriques de récupération
app.py                  interface Streamlit
docs/                   cahier des charges, plan de rapport
```

## Pistes d'amélioration

- Reranking avec un cross-encoder
- Découpage (chunking) de réponses longues
- Détection de la langue et réponse dans la langue de l'utilisateur
- Seuil de confiance : répondre « je ne sais pas » si la similarité est faible
- Évaluation de la génération (fidélité aux sources) avec un jeu annoté à la main
