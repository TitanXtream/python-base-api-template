from repos.user_repo import UserRepo

class UserService():
    
    def __init__(self,user_repo:UserRepo):
        self.__user_repo = user_repo
        pass
    
    def get_user_profile(self,user_id:str):
        return self.__user_repo.get_user_data(user_id)
        