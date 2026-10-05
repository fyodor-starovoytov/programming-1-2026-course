import logic
def run_program() -> None:
    while True:
        api = input("URL (enter for default): ")
        if api == "":
            api = "https://tim.jyu.fi/files/kurssit/it/iseai/26-27/programming1/material/files/1015427/lunches.json"

        restaurants_available = logic.fetch_restaurants(api)

        while True:
            restaurant = input("Restaurant (enter for list): ")
            if restaurant == "":
                logic.print_restaurant_names(api)
            elif logic.get_restaurant(restaurants_available, restaurant):
                print("Restaurant found")
                break
            else:
                print("Restaurant not found")

        diet = input("diet (enter for none): ")
        if diet == "":
            diet = None

        print("")
        logic.print_lunches(api, restaurant ,diet)

run_program()