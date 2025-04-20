import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

from schema.schema import *

print("Ładowanie zmiennych środowiskowych z pliku .env...")

load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    print("BŁĄD: Nie znaleziono zmiennej środowiskowej DATABASE_URL.")
    print("Upewnij się, że plik .env istnieje i zawiera DATABASE_URL.")
    exit(1)

print(f"Łączenie z bazą danych: {database_url.replace(os.getenv('DB_PASSWORD', 'PASSWORD'), '********')}")

try:
    engine = create_engine(database_url)

    print("Tworzenie tabel (jeśli nie istnieją)...")
    Base.metadata.create_all(bind=engine)

    print(">>> Sukces! Tabele zostały utworzone (lub już istniały).")

except Exception as e:
    print("\n>>> BŁĄD podczas tworzenia tabel:")
    print(e)
    exit(1)