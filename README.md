# Web Pentest Platform

**Avertissement légal : effectuez des tests uniquement sur des cibles que vous êtes autorisé à tester par écrit.**

Cette plateforme fournit une API FastAPI et une interface React pour lancer des outils de pentest Web via des workers Celery.

## Démarrage

```bash
git clone <repo>
cd scan-port
cp .env.example .env
docker compose up -d --build
```

API disponible sur http://localhost:8080/api/docs
Frontend sur http://localhost:5173

## Exemples

```bash
curl -X POST http://localhost:8080/api/scan/nuclei \
  -H "x-api-key: change-me" -H "Content-Type: application/json" \
  -d '{"target":{"value":"https://example.com"},"options":{"severity":["high","critical"]}}'
```

Les rapports sont stockés dans `data/reports/<job_id>/<tool>/`.

## Licence

Distribué sous licence MIT.
