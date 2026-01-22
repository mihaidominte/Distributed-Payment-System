from database import DatabaseServer
from server import Server

if __name__ == '__main__':
    db = DatabaseServer()
    """print(db.get("users", "1=1"))"""
    server = Server()
    server.start()