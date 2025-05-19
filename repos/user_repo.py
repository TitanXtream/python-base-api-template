from utils.static_test_data import users

class UserRepo:
    def __init__(self):
        self.db_repo = users
    
    def get_user_data(self,user_id:str):
        return next((item for item in self.db_repo if item.get("id") == user_id), None)