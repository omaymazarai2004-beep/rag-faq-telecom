# Plan du rapport

## 1. Introduction
Problème (questions récurrentes au service client), objectif, apport du RAG par rapport à un chatbot à règles ou à un LLM seul.

## 2. État de l'art
- Embeddings de phrases (Sentence-BERT) et similarité cosinus
- Recherche vectorielle (FAISS, index exact vs approximatif)
- Principe du RAG et limites (hallucinations, qualité de la récupération)

## 3. Données
Description de la FAQ, catégories, nettoyage, construction du jeu d'évaluation (reformulations).

## 4. Conception et architecture
Schéma du pipeline, choix du modèle d'embeddings, de l'index, du prompt et du seuil.

## 5. Implémentation
Structure du code, modules, interface Streamlit, mode dégradé.

## 6. Évaluation
- Hit@1, Hit@3, Hit@5, MRR
- Analyse des échecs : quelles questions échouent et pourquoi
- Comparaison : un autre modèle d'embeddings, avec/sans le texte de la réponse dans la vectorisation, avec/sans reranking
- Test hors périmètre : taux de faux positifs selon le seuil

## 7. Limites et perspectives
Taille de la FAQ, absence de mémoire de conversation, évaluation manuelle de la génération, déploiement.

## 8. Conclusion

## Annexes
Extraits de code, captures de l'interface, tableau des résultats.

---

## Questions probables en entretien (à préparer)

1. Pourquoi des embeddings multilingues plutôt qu'un TF-IDF ?
2. Pourquoi normaliser les vecteurs ? Quel lien avec le produit scalaire ?
3. Comment réduis-tu les hallucinations ?
4. Comment as-tu choisi le seuil de similarité ? Quel compromis entre rappel et précision ?
5. Que se passe-t-il avec 100 000 entrées ? (index approximatif IVF/HNSW, chunking)
6. Comment évaluerais-tu la qualité de la génération, pas seulement de la récupération ?
7. Quelles améliorations apporterais-tu ? (reranking, historique de conversation, détection de langue)
