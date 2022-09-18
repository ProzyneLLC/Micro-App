
from flask_login import UserMixin
from Website_Folder import DATABASEHELPER as DB
from Website_Folder import login_manager


class User(UserMixin):

    def __init__(self):
        self.email = None

    def get_id(self):
        try:
            try:
                return self.email
            except:
                userID = User()
                userID.email = self
                return userID
        except:
            return None


@login_manager.user_loader
def user_loader(user_id):

    return User.get_id(user_id)