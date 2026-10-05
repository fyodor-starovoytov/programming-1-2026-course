import json
from urllib.request import urlopen
from urllib.error import URLError

def fetch_restaurants(api: str) -> list[dict]:
    lst = []
    try:
        with urlopen(api) as connection:
            response = connection.read().decode('utf-8')
        data = json.loads(response)
        return data["results"]["en"]

    except Exception:
        raise OSError("Failed to load data from: " + api);

def get_restaurant(restaurants: list[dict], restaurant_name: str) -> dict:
    try:
        for restaurant in restaurants:
            if restaurant["name"].lower().startswith(restaurant_name.lower()):
                return restaurant
    except Exception:
        raise ValueError("Failed to find restaurant starting with: " + restaurant_name)

def get_hours(restaurant_data: dict) -> str:
    try:
        data =  restaurant_data["opening_hours"]
        if data == "":
            return "Unknown hours"
        return data
    except Exception:
        return "Unknown hours"

def fits_diet(lunch_option: list[dict], diet: str) -> bool:
    count = 0
    max_count = len(lunch_option)
    for item in lunch_option:
        for element in item["diets"]:
            if element.lower() == diet.lower():
                count += 1
    if count == max_count:
        return True
    return False

def get_lunch_options(restaurant_data: dict, diet: str | None = None) -> list[list[dict]]:
    lst = []
    data = restaurant_data["items"]
    if diet is None:
        return data
    else:
        for item in data:
            if fits_diet(item, diet):
                lst.append(item)
    return lst

def get_price(lunch_option: list[dict]) -> str:
    try:
        data = lunch_option[0]["price"]
        if data != "":
            return data
        else:
            return "Unknown price"
    except Exception:
        return "Unknown price"

def print_restaurant_names(api: str) -> None:
    data = fetch_restaurants(api)
    lst = []
    for element in data:
        if element != "":
            lst.append(element["name"])
    names = ""
    for item in lst:
        names += f"{item}, "
    print (names)

def describe_lunch_option(lunch_option: list[dict]) -> str:
    str = ""
    for i in range(len(lunch_option)):
        option = lunch_option[i]["name"]
        str += f"\t{option.strip()}\n"
    price = lunch_option[0]["price"]
    str += f"\t{price.strip()}\n"
    return str

def print_lunches(api: str, restaurant_name: str, diet: str | None = None) -> None:
    restaurants = fetch_restaurants(api)
    restaurant = get_restaurant(restaurants, restaurant_name)

    time = get_hours(restaurant)
    lunches = get_lunch_options(restaurant, diet)
    if len(lunches) == 0:
        print("No suitable lunches")
        return

    print(f"{restaurant['name']} ({time})")
    str = ""

    for j in lunches:
        for i in range(len(j)):
            option = j[i]["name"]
            str += f"\t{option.strip()}\n"
        price = j[0]["price"]
        str += f"\t{price.strip()}\n"

    print(str)