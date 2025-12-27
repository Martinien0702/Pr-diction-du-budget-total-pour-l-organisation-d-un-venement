# -----------------------------
# Image Python légère
# -----------------------------
FROM python:3.12-slim

# On évite les interactions dans le terminal
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Copier les requirements
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet dans le conteneur
COPY . .

# Expose Cloud Run port
EXPOSE 8080

# Start FastAPI with Uvicorn on the correct port
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
