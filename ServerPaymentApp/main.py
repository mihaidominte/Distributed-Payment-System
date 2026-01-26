import time
from database import DatabaseServer
from server import Server

if __name__ == '__main__':
    db = DatabaseServer()
    """print(db.get("users", "1=1"))"""
    new_user = {
        "id": 1,
        "public_key": "",
        "balance": 0.0,
        "password": "1234",
        "last_sync": int(time.time())
    }
    db.insert("users", new_user)
    server = Server()
    server.start()