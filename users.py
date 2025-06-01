class User:
    def __init__(self, username, password, role):
        self.__username = username
        self.__password = password
        self.__role = role

    def check_pass(self, in_password):
        return self.__password == in_password

    def get_username(self):
        return self.__username

    def get_password(self):   # thêm getter mật khẩu
        return self.__password

    def get_role(self):
        return self.__role

    def set_username(self, new_username):
        self.__username = new_username

    def set_password(self, new_password):
        self.__password = new_password

    def set_role(self, new_role):
        self.__role = new_role

    def to_dict(self):
        return {
            "username": self.__username,
            "password": self.__password,
            "role": self.__role
        }

    @staticmethod
    def from_dict(data):
        return User(data["username"], data["password"], data["role"])
