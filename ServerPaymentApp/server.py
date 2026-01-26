import socket
import threading
import json
import time
from database import DatabaseServer
from server_key_store import ServerKeyStore
import utils
from tokens_manager import TokensManager
from users_manager import UsersManager

server_key_store = ServerKeyStore()

def comm_interface(message: dict, db: DatabaseServer) -> dict | None:
    server_public_key = server_key_store.public_key
    tokens_manager = TokensManager(db)
    users_manager = UsersManager(db)
    pending_users = {}

    if message["activity"] == "new_user_start_config":
        new_user_id = utils.generate_new_user_id()
        pending_users[new_user_id] = time.time()
        response = {
            "activity": "config_id",
            "id": new_user_id,
            "public_key": server_public_key
        }
        return response

    elif message["activity"] == "new_user_final_config":
        try:
            if message["id"] not in pending_users:
                return {"activity": "fail", "reason": "invalid_flow"}
            new_user = {
                "id": message["id"],
                "public_key": message["public_key"],
                "balance": 0.0,
                "password": "1234",
                "last_sync": int(time.time())
            }
            if not db.get_one("users", "id = ?", (new_user["id"],)):
                db.insert("users", new_user)
                del pending_users[message["id"]]
                return {"activity": "success"}
            return {"activity": "fail", "reason": "user_exists"}
        except Exception as e:
            print("New user error:", e)
            return {"activity": "fail", "reason": f"{e}"}

    elif message["activity"] == "ledger_sync":
        chain_ok = tokens_manager.validate_user_blockchain(message["blockchain"])
        if chain_ok:
            new_genesis_token = tokens_manager.generate_genesis_token(message["id"])
            return {"activity": "success", "server_token": new_genesis_token}
        return {"activity": "fail"}

    elif message["activity"] == "send_money":
        if users_manager.identify_user(message["id"], message["password"]):
            result = users_manager.send_money(
                message["id"], message["amount"], message["sender_id"], message["receiver_id"])
            if result:
                return {"activity": "success"}
            else:
                return {"activity": "fail"}
        return {"activity": "fail"}

    elif message["activity"] == "receive_money":
        pass

    return None

def handle_client(conn, addr):
    print(f"[+] Client connected: {addr}")
    db = DatabaseServer()

    try:
        buffer = ""
        while True:
            data = conn.recv(1024)

            if not data:
                print("[DEBUG] recv() returned empty data → client closed connection")
                break

            try:
                decoded = data.decode()
            except UnicodeDecodeError as e:
                print(f"[ERROR] Decode failed: {e}")
                continue

            buffer += decoded

            while "\n" in buffer:
                raw, buffer = buffer.split("\n", 1)
                raw_stripped = raw.strip()

                print(f"[DEBUG] Raw message received: '{raw_stripped}'")

                if not raw_stripped:
                    continue

                try:
                    msg = json.loads(raw_stripped)
                except json.JSONDecodeError as e:
                    print(f"\033[91m[JSON ERROR]\033[0m {e}")
                    print(f"\033[91m[RAW DATA]\033[0m '{raw_stripped}'")
                    continue

                if not isinstance(msg, dict):
                    print(f"[ERROR] JSON is not a dict: {msg}")
                    continue

                print(f"[DEBUG] Parsed message: {msg}")

                response = comm_interface(msg, db)
                if response is not None:
                    conn.sendall((json.dumps(response) + "\n").encode())

    except Exception as e:
        print(f"\033[91m[FATAL ERROR]\033[0m {e}")
        import traceback
        traceback.print_exc()

    finally:
        print(f"[-] Client disconnected: {addr}")
        conn.close()
        db.close_database()


class Server:
    def __init__(self, host: str="", port: int=9999):
        self.HOST = host
        self.PORT = port
        self.server = None

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.HOST, self.PORT))
        self.server.listen()
        print(f"[START] Server started on {self.HOST}:{self.PORT}")

        while True:
            conn, addr = self.server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

