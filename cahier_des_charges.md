# Cahier des charges — Chatbot RAG sur FAQ télécom

## 1. Contexte et objectif

Les services clients télécom reçoivent un grand nombre de questions récurrentes (facturation, fibre, mobile, dépannage). L'objectif est de construire un assistant qui répond automatiquement à ces questions en s'appuyant sur une base de FAQ, sans inventer d'information.

## 2. Périmètre

**Inclus** : indexation d'une FAQ, recherche sémantique multilingue, génération de réponses sourcées, interface de démonstration, évaluation quantitative de la récupération.

**Exclus** : intégration à un système de production, authentification des clients, accès à des données personnelles de compte.

## 3. Exigences fonctionnelles

| ID | Exigence |
|----|----------|
| F1 | Charger et nettoyer une FAQ au format CSV |
| F2 | Retrouver les k entrées les plus proches d'une question (k réglable) |
| F3 | Générer une réponse en français fondée uniquement sur les entrées retrouvées |
| F4 | Afficher les sources (id, question, score de similarité) |
| F5 | Répondre « je ne sais pas » si aucune entrée n'est assez proche (seuil) |
| F6 | Fonctionner en mode dégradé (retrieval seul) sans clé d'API |
| F7 | Calculer Hit@k et MRR sur un jeu de questions reformulées |

## 4. Exigences non fonctionnelles

- Temps de réponse de la recherche inférieur à 1 seconde pour quelques milliers d'entrées
- Code modulaire, documenté, reproductible (requirements, README)
- Aucune donnée personnelle ou confidentielle dans le dépôt

## 5. Choix techniques

| Composant | Choix | Justification |
|-----------|-------|---------------|
| Embeddings | paraphrase-multilingual-MiniLM-L12-v2 | Léger, multilingue (fr/ar/en), tourne sur CPU |
| Index | FAISS IndexFlatIP | Exact, simple, suffisant à cette échelle |
| LLM | API Anthropic (optionnelle) | Qualité de rédaction ; remplaçable par un modèle local |
| Interface | Streamlit | Démo rapide |

## 6. Données

FAQ fictive de 20 entrées (5 catégories) fournie dans `data/faq.csv`, avec 20 questions de test reformulées dans `eval/questions.csv`. Pour un jeu plus riche : FAQ publique d'un opérateur (vérifier les conditions d'utilisation), ou FAQ rédigée par toi-même à partir d'un domaine que tu connais.

## 7. Critères d'acceptation

- Hit@3 supérieur ou égal à 0,85 sur le jeu de test
- Aucune réponse affirmative pour une question hors périmètre (test avec 5 questions hors sujet)
- Démo Streamlit fonctionnelle avec affichage des sources

## 8. Planning proposé (4 semaines)

| Semaine | Tâches |
|---------|--------|
| 1 | Prise en main des embeddings, nettoyage de la FAQ, premier index |
| 2 | Pipeline de recherche, jeu d'évaluation, premières métriques |
| 3 | Génération avec LLM, prompt, seuil de confiance, interface |
| 4 | Améliorations (reranking, chunking), tests hors périmètre, rapport, README |

## 9. Risques

| Risque | Mitigation |
|--------|------------|
| Hallucinations du LLM | Prompt restrictif, citation des sources, seuil de confiance |
| Questions hors périmètre | Seuil de similarité, réponse de repli |
| FAQ trop petite pour juger | Étendre à 100+ entrées, ajouter des reformulations |
