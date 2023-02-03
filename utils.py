import re
from typing import Iterator, Any, Callable, List
from constants import DATA_DIR


def log_generator() -> Iterator:
    """
    Генератор logs.txt
    """
    with open(DATA_DIR) as file:
        log_string: List[str] = file.readlines()
        for log in log_string:
            yield log


def user_filter(param: str, generate: Iterator[str]) -> Iterator[str]:
    """
    Функция user_filter является “поиском” по файлу, ее можно применять, например,
    когда нужно найти запрос с определенными параметрами или IP адресом
    С помощью filter() у добно искать вхождения строки
    """
    return filter(lambda x: param in x, generate)


def user_map(param: int, generate: Iterator[str]) -> Iterator[str]:
    """
    Функция изменяет формат исходных данных (проекция). param передает номер колонки.
    Исходные данные разделяются на колонки на основе пробела. В результате выполнения запроса должна быть
    выведена опред. колонка (все ip, все методы из логов и так далее)
    """
    return map(lambda string: string.split()[int(param)], generate)


def user_unique(generate: Iterator[str], *args: Any, **kwargs: Any) -> Iterator[str]:
    """
    Запрос cmd1=unique value1=””. У команды unique нет аргументов (в value1 нужно передать пустую строку)
    Функция отдает только уникальные значения
    """
    unique_list: List[str] = []
    for string in generate:
        if string not in unique_list:
            unique_list.append(string)
            yield string


def user_sort(param: str, generate: Iterator[str]) -> Iterator[str]:
    """
    Функция user_sort сортирует данные в алфавитном порядке или в обратном алфавитном порядке, в зависимости от
    переданного аргумента. asc - о меньшего к большему, desc - от большего к меньшему
    """
    return iter(sorted(generate, reverse=param == 'desc'))


def user_limit(param: str, generate: Iterator[str]) -> Iterator[str]:
    """
    Функция отдает опред. количество строк
    """
    counter = 1
    for string in generate:
        if counter > int(param):
            break
        counter += 1
        yield string


def regex_query(param: str, generate: Iterator[str]) -> Iterator[str]:
    """
    На вход функции подается РВ и Генератор logs.txt
    re.search(pattern, string, flags=0): просканирует строку в поисках первого совпадения с шаблоном регулярного
    выражения и вернет соответствующий объект совпадения. Вернет None, если никакая позиция в строке не соответствует
    шаблону.
    """
    pattern_regex: re.Pattern = re.compile(param)
    return filter(lambda string: re.search(pattern_regex, string), generate)


dict_of_utils: dict[str, Callable[..., Iterator[str]]] = {
    'filter': user_filter,
    'map': user_map,
    'unique': user_unique,
    'sort': user_sort,
    'limit': user_limit,
    'regex': regex_query,
}
