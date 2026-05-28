# Railway production Dockerfile
# Build frontend, then run backend with Waitress

FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Backend code
COPY backend/ .

# Frontend build
COPY --from=frontend-build /app/frontend/dist /app/frontend/dist

# Railway provides PORT env var
ENV PORT=5000

EXPOSE 5000

CMD ["python", "server.py"]
