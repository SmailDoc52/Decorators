def open_file_generator(file):
    file = open(file, 'a')
    try:
        yield file
    finally:
        file.close()