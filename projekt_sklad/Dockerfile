# Použij základní obraz Pythonu
FROM python:3.10-slim

# Nastav pracovní adresář v kontejneru
WORKDIR /sklad

# Zkopíruj soubor requirements.txt do kontejneru
COPY requirements.txt /sklad/

# Nainstaluj závislosti
RUN pip install --no-cache-dir -r requirements.txt

# Zkopíruj zbytek aplikace
COPY . /sklad/

# Nastav proměnnou prostředí pro Django
ENV PYTHONUNBUFFERED=1

# Exponuj port (např. 8000 pro Django)
EXPOSE 8000

# Spuštění serveru Django
CMD ["python", "manage.py", "runserver", "localhost:8000"]


