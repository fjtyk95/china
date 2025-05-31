# cross-border-trade-lens

This project contains a Next.js frontend and a FastAPI backend with Celery.

## Development

Start services with docker-compose:

```bash
docker-compose up --build
```

The API is available at http://localhost:8000 and Celery worker connects to Redis.

Example Celery task:

```python
from app.tasks import add
add.delay(2, 3)
```
