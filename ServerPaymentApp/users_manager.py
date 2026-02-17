import utils
from database import DatabaseServer

class UsersManager:
    def __init__(self, db: DatabaseServer):
        self.db = db

    def new_user_config(self):
        pass

    def identify_user(self, user_id: str) -> bool:
        user = self.db.get_one("users", "id = ?", (user_id,))
        if not user:
            utils.print_error("User not found")
            return False
        return True

    def send_money(self, user_id: str, amount: float, sender_id: str, receiver_id: str) -> bool:
        if user_id != sender_id:
            utils.print_error("User cannot be different from sender")
        user = self.db.get_one("users", "id = ?", (user_id,))
        receiver = self.db.get_one("users", "id = ?", (receiver_id,))
        if not receiver:
            utils.print_error("Receiver not found")
            return False
        if user["balance"] < amount:
            utils.print_error("Insufficient funds")
            return False
        user["balance"] -= amount
        receiver["balance"] += amount
        self.db.update("users", [user, receiver])
        return True

    def receive_money(self):
        pass

    def update_user_info(self):
        pass

    def update_user_balance(self):
        pass

