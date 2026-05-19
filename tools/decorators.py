import json
from functools import wraps
from datetime import datetime


def logger(old_function):
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
        with open('main.log', 'a', encoding='utf-8') as file:
            json.dump(log_dict, file, ensure_ascii=False)
            file.write('\n')
        return result
    return new_function


def logger_with_path(path):
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
            with open(path, 'a', encoding='utf-8') as f:
                json.dump(log_dict, f, ensure_ascii=False)
                f.write('\n')
            return result
        return new_function
    return __logger