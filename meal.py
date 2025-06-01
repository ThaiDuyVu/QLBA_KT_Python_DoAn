from datetime import datetime

class Meal :
    def __init__(self,main_dish , side_dish, third_dish, soub, dessert, carbo,  time):
        self.main_dish = main_dish 
        self.side_dish = side_dish
        self.third_dish = third_dish
        self.soub = soub
        self.dessert = dessert 
        self.carbo = carbo 
        self.time = time 
    def to_dict(self) :
        return {
            "main_dish" :self.main_dish,
            "side_dish" :self.side_dish,
            "third_dish": self.third_dish, 
            "soub" :self.soub,
            "dessert" :self.dessert, 
            "carbo":self.carbo, 
            "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
    @staticmethod
    def from_dict(data) : 
        return Meal(data["main_dish"], data["side_dish"], data["third_dish"], data["soub"], data["dessert"],data["carbo"],data["time"])  