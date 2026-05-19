from tools.csv_manager import CSVManager


if __name__ == "__main__":
    path = 'log_CSVManager.log'
    source_file = CSVManager("phonebook_raw.csv")
    finished_file = CSVManager("phonebook.csv")

    lines = source_file.csv_reader()
    
    headers = next(lines)
    result_dict = {}
    
    for line in lines:
        fio = ' '.join(line[:3]).strip().split()
        if len(fio) < 3:
            fio.append('')
    
        unique_name = (fio[0], fio[1])
        new_data = [
            fio[2], 
            line[3], 
            line[4], 
            CSVManager.cleaned_phone(line[5]), 
            line[6]
        ]
        
        if unique_name not in result_dict:
            result_dict[unique_name] = new_data
        else:
            data = result_dict.get(unique_name)
            
            for i in range(len(data)):
                if not data[i] and new_data[i]:
                    data[i] = new_data[i]
    
    finished_file.csv_writer(result_dict, headers)
