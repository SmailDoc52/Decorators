import csv
import re

from tools.decorators import logger_with_path as logger


class CSVManager:
    def __init__(self, file):
        self.file = file

    def csv_reader(self):
        with open(self.file, encoding='utf-8') as f:
            lines = csv.reader(f, delimiter=',')
            for line in lines:
                try:
                    yield line
                except StopIteration as e:
                    return StopIteration

    def csv_writer(self, data_dict: dict, headers):
        with open(self.file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for key, value in data_dict.items():
                data = {
                    'lastname': key[0],
                    'firstname': key[1],
                    'surname': value[0],
                    'organization': value[1],
                    'position': value[2],
                    'phone': value[3],
                    'email': value[4],
                }
                writer.writerow(data.values())

    @staticmethod
    @logger('csv_manager.log')
    def cleaned_phone(phone):
        if phone:
            phone_pattern = (
                r"(\+7|8)?\s*-?\(?(\d{3})\)?\s*-?(\d{3})\s*-?"
                r"(\d{2})\s*-?(\d{2})\s*\(?(доб)?.?\s*(\d+)?\)?"
            )
            replace_pattern = r"+7(\2)\3-\4-\5 \6.\7"
            result = re.sub(phone_pattern, replace_pattern, phone)
            return result.strip(' .\n')
        return phone
    