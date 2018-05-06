try:
    with open('myfile.txt2') as fh:
        file_data = fh.read()
    print(file_data)
except FileNotFoundError:
    print('The data file is missing.')
except PermissionError:
    print('The is not allowed.')
except Exception as err:
    print('Some other error occured. ', str(err))



