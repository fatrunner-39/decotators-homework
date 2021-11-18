from datetime import datetime
import json
import os
import requests


def make_trace(log_path):
    def _make_trace(old_function):
        def new_function(*args, **kwargs):
            data = dict()
            data["Дата запуска фунции:"] = str(datetime.now())
            data["Имя функции:"] = old_function.__name__
            data["Аргументы:"] = args
            result = old_function(*args, **kwargs)
            data["Возвращенное значение:"] = result
            with open(log_path, 'a', encoding='utf-8') as outfile:
                json.dump(data, outfile, ensure_ascii=False, indent=4)
                outfile.write(',\n')
            print(f"Путь к логам: {os.path.abspath('data.json')}")
            return data

        return new_function

    return _make_trace


# Логгер к произвольной функции
@make_trace(os.path.abspath('data.json'))
def sum_args(*args):
    summa = 0
    for el in args:
        summa += el
    return summa


sum_args(1, 2, 3, 4)

# Логгер к функции из ДЗ по библиотеке requests
@make_trace(os.path.abspath('data.json'))
def the_most_iintellegence(superheroes):
    heroes_dict = {}
    max_point = 0
    name = None
    for hero in superheroes:
        url = "https://superheroapi.com/api/2619421814940190/search/"
        name = hero
        response = requests.get(url + name, timeout=5)
        intellect = response.json()['results'][0]['powerstats']['intelligence']
        heroes_dict[hero] = intellect
    for key, value in heroes_dict.items():
        if int(value) > max_point:
            max_point = int(value)
            name = key
    # print(key, max_point)

    return f'Самый умнный супергерой {name}! \nЗначение "intelligence" равно {max_point}.'


print(the_most_iintellegence(["Hulk", "Captain America", "Thanos"]))