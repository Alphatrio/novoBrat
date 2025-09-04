# novoBrat

## Structure du projet
- `backend/` : API Flask minimale pour l'import, l'annotation et l'export de textes.
- `frontend/` : interface web statique pour annoter les documents.
- `tests/` : tests unitaires des modèles et de la base de données.

## Prérequis
- Python 3.11+
- `pip` pour installer les dépendances du backend
- (Optionnel) Docker et Docker Compose pour un démarrage rapide

## Installation
### Avec Docker
1. Construire et lancer les services :
   ```bash
   docker compose up
   ```
2. Le backend est disponible sur `http://localhost:5000` et le frontend sur `http://localhost:8080`.

### Installation manuelle
1. Installer les dépendances du backend :
   ```bash
   pip install -r backend/requirements.txt
   ```
2. Démarrer le backend :
   ```bash
   python backend/app.py
   ```
3. Servir le frontend statique (par exemple via Python) :
   ```bash
   python -m http.server 8080 --directory frontend
   ```

## Exemple d'utilisation
1. **Importer un texte** :
   ```bash
   curl -X POST http://localhost:5000/documents \
        -H "Content-Type: application/json" \
        -d '{"text": "Bonjour monde"}'
   ```
2. **Annoter** :
   - Ouvrir `http://localhost:8080` dans un navigateur.
   - Sélectionner une portion du texte et choisir un label.
3. **Exporter les annotations** :
   ```bash
   curl http://localhost:5000/annotations
   ```
   Les annotations sont retournées au format JSON.

## Tests
Lancer l'ensemble des tests avec :
```bash
pytest
```

