import os
import json
from functools import wraps
from datetime import datetime

from tools.open_file import open_file_generator


def logger(file):
    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            date = str(datetime.now())
            arguments = [elem for elem in [args, kwargs] if elem]
            name_func = old_function.__name__
            log_dict = {
                'date_time': date,
                'func': name_func, 
                'function arguments': arguments, 
                'result': result, 
            }
            json.dump(log_dict, file)
            file.write('\n')
            file.flush()
            return result
        return new_function
    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')
    
    for path in paths:
        if os.path.exists(path):
            os.remove(path)
    
    file_object = open_file_generator('log_1.log')
    file_object2 = open_file_generator('log_2.log')
    file_object3 = open_file_generator('log_3.log')
    
    file1 = next(file_object)
    file2 = next(file_object2)
    file3 = next(file_object3)
    
    files = (file1, file2, file3)

    for path, file in zip(paths, files):

        @logger(file)
        def hello_world():
            return 'Hello World'

        @logger(file)
        def summator(a, b=0):
            return a + b

        @logger(file)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), (
            "Функция возвращает 'Hello World'"
        )
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, (
                f'{item} должен быть записан в файл'
            )


if __name__ == '__main__':
    test_2()