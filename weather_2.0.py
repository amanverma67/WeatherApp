#weather,py
import argparse
import json
import sys
from configparser import ConfigParser
from urllib import error, parse, request
from pprint import pp
import style

BASE_WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

THUNDERSTORM = range(200, 300)
DRIZZLE = range(300, 400)
RAIN = range(500, 600)
SNOW = range(600, 700)
ATMOSPHERE = range(700, 800)
CLEAR = range(800, 801)
CLOUDY = range(801, 900)

'''
PADDING = 20
REVERSE = "\033[;7m"
RESET = "\033[0m"
'''
def _get_api_key():
    """Fetch the API key from your configuration file.

    Expects a configuration file named "secrets.ini" with structure:

        [openweather]
        api_key=<YOUR-OPENWEATHER-API-KEY>
    """
    config = ConfigParser()
    config.read(r'C:\Users\Aman_Verma3\iCloudDrive\Bulbul\Weather-App\secrets.ini')
    return config["openweather"]["api_key"]
'''
def read_user_cli_args():
    """Handles the CLI user interactions.
    Returns:
        argparse.Namespace: Populated namespace object
    """
    parser = argparse.ArgumentParser(
        description="gets weather and temperature information for a city"
    )
    parser.add_argument(
        "city", nargs= "+", type=str, help="Enter the city name"
    )
    parser.add_argument(
        "-i",
        "--imperial",
        action="store_true",
        help="display the temperature in imperial units",
    )
    return parser.parse_args()
'''
def build_weather_query(city_input, imperial=False):
    """Builds the URL for an API request to OpenWeather's weather API.

    Args:
        city_input (List[str]): Name of a city as collected by argparse
        imperial (bool): Whether or not to use imperial units for temperature

    Returns:
        str: URL formatted for a call to OpenWeather's city name endpoint
    """
    api_key = _get_api_key()
    url_encoded_city_name = parse.quote_plus(city_input)
    units = "imperial" if imperial else "metric"
    url = (f"{BASE_WEATHER_API_URL}?q={url_encoded_city_name}"
           f"&units={units}&appid={api_key}"
    )
    return url

def get_weather_data(query_url):
    """Makes an API request to a URL and returns the data as a Python object.

    Args:
        query_url (str): URL formatted for OpenWeather's city name endpoint

    Returns:
        dict: Weather information for a specific city
    """
    try:
        response = request.urlopen(query_url)
    
    except error.HTTPError as http_error:
        if http_error.code == 401:
            sys.exit("Access denied. Check your API key.")
        elif http_error.code == 404:
            print("Can't find weather data for this city.")
            return None  # Return None to indicate an error occurred
        else:
            sys.exit(f"Something went wrong... ({http_error.code})")
    
    data = response.read()
    
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        sys.exit("Couldn't read the server response.")



def display_weather_info(weather_data, imperial=False):
    city = weather_data["name"]
    weather_id = weather_data['weather'][0]['id']
    weather_description = weather_data["weather"][0]["description"]
    temperature = weather_data["main"]["temp"]
    feels_like = weather_data["main"]["feels_like"]

    style.change_color(style.REVERSE)
    print(f"{city:^{style.PADDING}}", end="")
    style.change_color(style.RESET)
    
    weather_symbol, color = _select_weather_display_params(weather_id)  
    style.change_color(color)
    print(f"\t{weather_symbol}", end='')
    print(f" {weather_description.capitalize()}", end=" ")
    style.change_color(style.RESET)
    print(f"\t{temperature}°{'F' if imperial else 'C'}", end=" ")
    print(f"\tFeels Like: {feels_like}°{'F' if imperial else 'C'}")

def _select_weather_display_params(weather_id):
    if weather_id in THUNDERSTORM:
        display_params = ("💥", style.RED)
    elif weather_id in DRIZZLE:
        display_params = ("💧", style.CYAN)
    elif weather_id in RAIN:
        display_params = ("💦", style.BLUE)
    elif weather_id in SNOW:
        display_params = ("⛄️", style.WHITE)
    elif weather_id in ATMOSPHERE:
        display_params = ("🌀", style.BLUE)
    elif weather_id in CLEAR:
        display_params = ("🔆", style.YELLOW)
    elif weather_id in CLOUDY:
        display_params = ("💨", style.WHITE)
    else:  # In case the API adds new weather codes
        display_params = ("🌈", style.RESET)
    return display_params

if __name__ == "__main__":
    print("Welcome to the Weather Information Program!")
    
    while True:
        proceed = input("Do you want to proceed(p) or quit(q): ") 
        
        if proceed == 'p':
            city_in = input("Enter the city name: ")
            imperial_input = input("Do you want to display the temperature in imperial units? (y/n): ")
            while True:
                if imperial_input.lower() == "y":
                    imperial = True
                    break
                elif imperial_input.lower() == 'n':
                    imperial = False
                    break
                else: 
                    print("Invalid input")
                    imperial_input = input("Valid inputs are 'y' or 'n' only: ")
                    
            query_url = build_weather_query(city_in, imperial)
            weather_data = get_weather_data(query_url)
            if weather_data is not None:
                display_weather_info(weather_data, imperial)
        elif proceed == 'q':
            sure = input("Are you sure?(y/n):")
            if sure == 'y':
                print("Goodbye!")
                quit()
            elif sure == 'n': 
                continue
            else:
                print("Invalid input")
                continue
        else:
            print("Invalid input")
            print("Valid inputs are 'p' or 'q' only")
            continue
