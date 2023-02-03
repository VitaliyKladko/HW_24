import os
from flask import Blueprint, request, jsonify, Response
from typing import Optional, Callable, Iterator, Tuple
from utils import log_generator, dict_of_utils
from constants import BASE_DIR, DATA_DIR


main_bp: Blueprint = Blueprint('main', __name__)


@main_bp.route('/perform_query', methods=['POST'])
def perform_query() -> Tuple[Response, int] | Response:
    json_query: Optional[dict] = request.json
    file_name: Optional[str] = json_query.get('filename')

    if not file_name:
        file_name = DATA_DIR

    if not os.path.exists(BASE_DIR + '/data/' + file_name):
        return Response('Файл не найден', status=400)

    commands_and_values: Optional[list] = json_query.get('queries')
    cmd_1, value_1 = commands_and_values[0].values()
    cmd_2, value_2 = commands_and_values[1].values()

    default_generator = log_generator()

    first_func: Optional[Callable] = dict_of_utils.get(cmd_1)
    second_func: Optional[Callable] = dict_of_utils.get(cmd_2)

    result: Optional[Iterator[str]] = None
    if first_func is not None:
        result = first_func(param=value_1, generate=default_generator)
        if second_func is not None:
            result = second_func(param=value_2, generate=result)
    return jsonify(list(result)), 200
