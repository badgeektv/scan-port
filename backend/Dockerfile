FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml ./
RUN pip install -r <(python - <<'PY'
import tomllib,sys
print('\n'.join(tomllib.load(open('pyproject.toml','rb'))['project']['dependencies']))
PY
) || true
COPY app ./app
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8080"]
