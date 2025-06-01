import json
import os
from users import User 
from meal import Meal 

class dataService :
    @staticmethod
    def load_data(filePath) :
        if not os.path.exists(filePath) :
            return []
        with open(filePath,'r',encoding="utf-8") as file :
            return json.load(file)
        
    @staticmethod
    def save_data(filePath, newdata) :
        oldData = dataService.load_data(filePath)
        if isinstance(newdata, dict):
            oldData.append(newdata)
        elif isinstance(newdata, list) :
            oldData.extend(newdata)
        
        with open(filePath, 'w',encoding="utf-8") as file : 
            json.dump(oldData, file, indent = 4 )

    #hàm ghi đè dữ liệu 
    @staticmethod 
    def save_data_write(filePath, data):
        with open(filePath, 'w', encoding='utf-8') as f:  # ✅ dùng 'w' để ghi đè
            json.dump(data, f, indent=4, ensure_ascii=False)
            
# class Kiểm tra đăng nhập 
class authService : 
    def __init__(self , user_file) :
        self.user_file = user_file
        self.users = [User.from_dict(u) for u in dataService.load_data(user_file)]
        
    def authenticate(self , username, password) : 
        for user in self.users : 
            if user.get_username() == username and user.check_pass(password) : 
                return user
        return None
    
    def registerAuthenticate(self , username, password) : 
        for user in self.users : 
            if user.get_username() == username : 
                return None
        newuser = User(username, password , "client")
        self.users.append(newuser)
        return newuser
# class xử lý món ăn 
class mealService :
    def __init__(self, meal_file) : 
        self.meal_file = meal_file 
        self.meals = [Meal.from_dict(u) for u in dataService.load_data(meal_file)]
        

    #----- lấy tên file chứa dữ liệu món ăn của user, nếu chưa có thì tạo file có định dạng như dưới: ------
    @staticmethod
    def get_user_meal_file(username) : 
        filename = f"data_{username}.json"
        if not os.path.exists(filename) :
            with open(filename, 'w') as file :
                json.dump([], file)
        return filename

        
