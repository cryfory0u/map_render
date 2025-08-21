import sqlite3
import os
from config import DB_NAME


class MapRepository:
    def __init__(self, db_path=DB_NAME):
        self.db_path = db_path
        if not os.path.exists(os.path.dirname(db_path)) and os.path.dirname(db_path):
            os.makedirs(os.path.dirname(db_path))

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_table(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS maps (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mapname TEXT NOT NULL UNIQUE,
                    mapstyle TEXT NOT NULL,
                    gjson TEXT NOT NULL
                )
            """)

    def upsert_map(self, mapname, mapstyle_content, gjson_content):
        sql = """
            INSERT INTO maps (mapname, mapstyle, gjson) VALUES (?, ?, ?)
            ON CONFLICT(mapname) DO UPDATE SET
                mapstyle=excluded.mapstyle,
                gjson=excluded.gjson;
        """
        with self._get_connection() as conn:
            conn.execute(sql, (mapname, mapstyle_content, gjson_content))
            print(f"Данные для '{mapname}' успешно загружены/обновлены.")

    def get_map_data(self, mapname):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT mapstyle, gjson FROM maps WHERE mapname = ?", (mapname,))
            return cursor.fetchone()
