import requests

def get_weather(city="Ho_Chi_Minh"):
    url = f"https://wttr.in/{city}?format=3"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text
        else:
            return f"Lỗi: {response.status_code}"
    except Exception as e:
        return f"Lỗi: {str(e)}"
