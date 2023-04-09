'''Program that takes data from load_data files
Implementation dictionary info and drawing map and location'''
import os
import sys
import folium
import webbrowser
from load_data import load_data
import matplotlib.pyplot as plt


def plot_ships_on_map(ships, zoom_start=3):
    '''Create Map for location'''
    # Calculate to Set Map Center
    total_lat = sum(float(ship['LAT']) for ship in ships)
    total_lon = sum(float(ship['LON']) for ship in ships)
    map_center = [total_lat / len(ships), total_lon / len(ships)]
    # Opening zoom area from calculated map_center
    ships_map = folium.Map(location=map_center, zoom_start=zoom_start)
    # Add a marker for each ship
    for ship in ships:
        folium.Marker(location=[float(ship['LAT']), float(ship['LON'])],
                      tooltip=ship['SHIPNAME']).add_to(ships_map)

    # Display the map in the default web browser
    map_html = ships_map.get_root().render()
    with open('ship_map.html', 'w', encoding='utf-8') as file_obj:
        file_obj.write(map_html)
    webbrowser.open('file://' + os.path.realpath('ship_map.html'))

    return 'Check your default browser'


def speed_histogram(ships_list):
    ''' Extract the speed information for all the ships'''
    filename = 'speed_histogram.png'
    speeds = []
    for ship in ships_list:
        speed = float(ship['SPEED'])
        speeds.append(speed)

    # Create a histogram of the speeds
    plt.hist(speeds, bins=20)
    plt.title('Speeds of Ships')
    plt.xlabel('Speed (knots)')
    plt.ylabel('Frequency')
    plt.show()

    # Save the histogram to a file
    plt.savefig(filename)
    plt.close()


def not_dublicate_list(ship_list):
    '''Print Without Dublicate Countries'''
    countries = set(map(lambda ship: ship['COUNTRY'], ship_list))
    template = ''  # function returns this string
    for i, country in enumerate(countries):
        names = []
        for ship in ship_list:
            # Catch the matching ship name in set of countries and move that data to another list
            if ship['COUNTRY'] == country:
                names.append(ship["SHIPNAME"])
        if names:
            # printing first name relatively others too
            template += f'{i+1}. ShipName: {names[0]} -> Country: {country}\n'
    return template


def countries_ships(ships_list):
    '''Print name and countries all in record'''
    template = ''
    sorted_countries = sorted(ships_list, key=lambda ship: ship['COUNTRY'])
    for i, ship in enumerate(sorted_countries):
        template += \
            f'{i+1}. Country: {ship["COUNTRY"]} -> ShipName: {ship["SHIPNAME"]}\n'
    template += f'Number of Ships: {len(ships_list)}\n'
    return template


def show_countries(ship_list):
    '''Print Only Countries Alphabetically'''
    countries = set(map(lambda ship: ship['COUNTRY'], ship_list))
    countries = sorted(countries)
    template = ''
    for i, country in enumerate(countries):
        template += f'{i+1}. {country}\n'
    return template


def ships_by_types(ship_list):
    '''Print Count of Active Ship Types'''
    type_dict = {}
    for ship in ship_list:
        if ship['TYPE_SUMMARY'] not in type_dict:
            type_dict[ship['TYPE_SUMMARY']] = 0
        type_dict[ship['TYPE_SUMMARY']] += 1
    template = ''
    i = 1
    for key, val in type_dict.items():
        template += f'{i}. {key}: {val}\n'
        i += 1
    return template


def top_countries(ship_list):
    '''Print N times countries where have more ships'''
    number_to_print = read_int('How many number to print: ')
    country_ships = {}
    for ship in ship_list:
        if ship['COUNTRY'] not in country_ships:
            country_ships[ship['COUNTRY']] = 0
        country_ships[ship['COUNTRY']] += 1
    sorted_list = sorted(
        country_ships.items(), key=lambda ship: (-ship[1], ship[0]))
    print_list = sorted_list[:number_to_print]
    i = 1
    template = ''
    for country, val in print_list:
        template += f'{i}.  {country} has {val} ships\n'
        i += 1
    return template


def list_string(alist):
    '''Return list of function as string'''
    alist_str = ''
    for func in alist:
        alist_str += func.__name__ + ', '
    return alist_str


def menu_string():
    '''Command Line For User
    Creating string according how dictionary appears'''

    command = {'countries': show_countries,
               'sort ships': top_countries,
               'country ship': not_dublicate_list,
               'active ships': countries_ships,
               'type summary': ships_by_types,
               'search ship': search_ship,
               'speed histogram': speed_histogram,
               'location': plot_ships_on_map,
               'exit': exit_program
               }
    print('\nAVAILABLE COMMANDS:')
    for key, func in command.items():
        if isinstance(func, list):
            print(f'\t{key}: {list_string(func)}')  # keep it ready
        else:
            print(f'\t{key}: {func.__name__}')
    user_req = read_text('\nEnter your command: ')
    user_req = user_req.lower().strip()
    if user_req in command and user_req != 'functions':
        return command[user_req]
    return f'{user_req} is not in command'


def search_ship_by_name(ship_name, ship_list):
    '''Searching given name '''
    search_list = []
    for ship in ship_list:
        if ship_name in ship['SHIPNAME']:
            search_list.append(ship['SHIPNAME'])
    return search_list


def search_ship(ship_list):
    '''Get the name string and call engine function to search'''
    ship_name = read_text('Enter the Ship Name: ')
    ship_name = ship_name.upper().strip()
    result = search_ship_by_name(ship_name, ship_list)
    if result:
        result_map = map(str, result)
        result_str = '\n'.join(result_map)
        return result_str
    return f'{ship_name} was not found'


def test():
    '''Test for functions'''
    test_data = load_data()
    ships = test_data['data']
    ships_for_test = []
    for i, ship in enumerate(ships):
        if i < 1:
            ships_for_test.append(ship)
    print(ships_for_test)


def read_text(prompt):
    '''Ignores Ctrl + C Keyboard Interruption'''
    while True:
        try:
            text = input(prompt)
            return text
        except KeyboardInterrupt:
            print('Do not attempt to stop program')


def read_int(prompt):
    '''Only accept integer entries and Ignore Ctrl + C'''
    while True:
        try:
            text = read_text(prompt)
            return int(text)
        except ValueError:
            print('Please Enter Integer Number')


def exit_program(ships_list):
    '''Function to exit the program'''
    ships_list = []
    print('Exiting program...')
    sys.exit()


def main():
    '''Function flow block'''
    all_data = load_data()
    ships = all_data['data']  # list
    while True:
        try:
            chosen_func = menu_string()
            print(chosen_func(ships))
        except TypeError as t_error:
            print(f"Check your command , {t_error}")


if __name__ == '__main__':
	main()
