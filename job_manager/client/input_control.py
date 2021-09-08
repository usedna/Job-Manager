from client import errors
import os

valid_extensions = ['jpg', 'jpeg', 'gif']
file = {'input': False, 'path': False, 'format': False}


def checkFormat(extension):
    try:
        if not extension or extension not in valid_extensions:
            raise errors.InvalidFormatError
        file['format'] = True
    except errors.InvalidFormatError:
        print("Error: Can't support this format")
    finally:
        return file['format']


def checkPath(path):
    try:
        if os.path.isdir(path):
            raise IsADirectoryError
        if not os.path.isfile(path):
            raise FileNotFoundError
        extension = path.split('.')[-1]
        file['path'] = checkFormat(extension)
    except IsADirectoryError:
        print("Error: Invalid path")
    except FileNotFoundError:
        print("Error: The path is wrong.")
    finally:
        return file['path']


def checkPathInput(path):
    try:
        if path.isspace():
            raise errors.InvalidInputError
        file['input'] = checkPath(path)
    except errors.InvalidInputError:
        print('You need to enter the path to the images directory\n')
    finally:
        return file['input']


def check_par(par):
    try:
        par = int(par)
    except ValueError:
        print("Invalid input")
        par = type(par)
    finally:
        return par


def get_par(par_name):
    par = check_par(input("Please provide {}: \n".format(par_name)))
    while str(type(par)) != """<class 'int'>""":
        par = check_par(input("Please provide {}: \n".format(par_name)))
    return par


def get_path():
    path = input("Please enter the path to the images directory: ")
    while not checkPathInput(path):
        path = input("Please enter the path to the images directory: ")
    return path


def checkCoordinates(x_y):
    is_good = False
    try:
        if len(x_y) != 2:
            raise errors.OutOfRangeError
        int(x_y[0])
        int(x_y[0])
        is_good = True
    except errors.OutOfRangeError:
        print("You must enter 2 arguments")
    except ValueError:
        print("Invalid input")
    finally:
        return is_good


def get_coordinate(text):
    coord = input('Please insert coordinate for {}'.format(text)).split()
    while not checkCoordinates(coord):
        coord = input('Please insert coordinate for {}'.format(text)).split()
    return coord
