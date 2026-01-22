import os
import sqlite3

class DatabaseServer:
    def __init__(self, database: str="Databases/server.db"):
        os.makedirs("Databases", exist_ok=True)

        self.conn = sqlite3.connect(
            database,
            timeout=10,
            check_same_thread=True
        )

        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.conn.execute("PRAGMA journal_mode = WAL;")

        self.init_tables()


    def init_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id TEXT PRIMARY KEY,
            password TEXT,
            public_key TEXT,
            balance REAL,
            last_sync INTEGER
        );
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tokens(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            sender_id TEXT,
            receiver_id TEXT,
            amount REAL,
            date INTEGER,
            hash TEXT,
            signature TEXT,
            counter_sig TEXT,
            previous_hash TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        """)
        self.conn.commit()

    def insert(self, table: str, entity: dict):
        cols = ", ".join(entity.keys())
        vals = tuple(entity.values())
        placeholders = ", ".join(["?"] * len(vals))
        self.cursor.execute(f"INSERT OR REPLACE INTO {table} ({cols}) VALUES ({placeholders})", vals)
        self.conn.commit()

    def get(self, table: str, where: str, params: tuple = ()):
        rows = self.cursor.execute(
            f"SELECT * FROM {table} WHERE {where}",
            params
        ).fetchall()
        return [dict(row) for row in rows]

    def get_one(self, table: str, where: str, params: tuple = ()):
        rows = self.get(table, where, params)
        return rows[0] if rows else None

    def update(self, table: str, entities: list[dict]):
        for entity in entities:
            entity_id = entity["id"]
            data = {k: v for k, v in entity.items() if k != "id"}

            set_part = ", ".join([f"{key}=?" for key in data.keys()])
            vals = tuple(data.values())

            self.cursor.execute(
                f"UPDATE {table} SET {set_part} WHERE id = ?",
                vals + (entity_id,)
            )
        self.conn.commit()

    def delete(self, table: str, entities: list[dict]):
        for entity in entities:
            entity_id = entity["id"]
            self.cursor.execute(f"DELETE FROM {table} WHERE id = ?", (entity_id,))
        self.conn.commit()

    def close_database(self):
        self.conn.close()