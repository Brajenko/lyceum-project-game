import csv
from operator import itemgetter

HEADERS = ['nickname', 'result']


def check_file():
    try:
        open('results.csv').close()
    except FileNotFoundError:
        with open('results.csv', encoding="utf8", mode='w') as res:
            writer = csv.DictWriter(res, delimiter=';', fieldnames=HEADERS, quotechar='"')
            writer.writeheader()


def write_new(nick: str, result: int) -> None:
    check_file()
    with open('results.csv', encoding="utf8", mode='a') as res:
        writer = csv.DictWriter(res, delimiter=';', fieldnames=HEADERS, quotechar='"')
        writer.writerow({'nickname': nick, 'result': result})
        res.close()


def get_best() -> (str, int):
    check_file()
    with open('results.csv', encoding="utf8") as res:
        reader = csv.DictReader(res, delimiter=';', quotechar='"')
        try:
            best_res = max(reader, key=lambda x: int(x['result']))
            return dict_to_tuple(best_res)
        except ValueError:
            return None


def get_last() -> (str, int):
    check_file()
    with open('results.csv', encoding="utf8") as res:
        reader = csv.DictReader(res, delimiter=';', quotechar='"')
        return dict_to_tuple(list(reader)[-1])


def dict_to_tuple(d: dict) -> (str, int):
    return itemgetter(*d.keys())(d)
