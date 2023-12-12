"""
Case-study №6
Developers: Kuznetsov N. 100%
            Shishko S. 70%
"""
import os

MENU = ['1. Просмотр каталога' ,
       '2. На уровень вверх' ,
       '3. На уровень вниз' ,
       '4. Количество файлов и каталогов' ,
       '5. Размер текущего каталога (в байтах)' ,
       '6. Поиск файла' ,
       '7. Запуск файла',
       '8. Выход из программы']
distance = 60

def doubleOutput(list1 = [], list2 = MENU, distance = 60, withInfo = 2):
    """
    Prints 2 lists in 2 columns.
    :param list1: left list
    :param list2: right list
    :param distance: number of symbols between lists
    :param withInfo: 0: not print info
                     1: print only directory
                     2: print directory with image
    :return:
    """
    if list1 == None:
        list1 = []
    elif type(list1) is not list:
        list1 = [list1]
    if list2 == None:
        list2 = []
    elif type(list2) is not list:
        list2 = [list2]

    if withInfo == 2:
        info = [' 💾 ' + os.getcwd() + '  ']
        list1 = info + list1
    elif withInfo == 1:
        info = [os.getcwd()]
        list1 = info + list1

    for i in range(len(list1)):
        if len(list1[i]) >= distance:
            list1[i] = list1[i][:distance-6]+'…'+ '  '


    if len(list1) >= len(list2):
        for i in range(len(list1)):
            if len(list1) - i <= len(list2):
                print(list1[i] + ' ' * (distance - len(list1[i])) + list2[i + len(list2) - len(list1)])
            else:
                print(list1[i])
    else:
        for i in range(len(list2)):
            if len(list2) - i <= len(list1):
                print(list1[i + len(list1) - len(list2)] + ' ' * (
                            distance - len(list1[i + len(list1) - len(list2)])) + list2[i])
            else:
                print(' ' * distance + list2[i])

def acceptCommand():
    """
    Returns input value from 1 to 8.
    :return: menu item
    :rtype: int
    """
    while True:
        try:
            item = int(input(' '*distance+'Выберите пункт меню: '))
            if 1 <= item <=8:
                return item
                break
            else:
                print(' '*distance+'Введите значение от 1 до 8')
        except:
            print(' '*distance+'Введите число')

def runCommand(command):
    """
    Starts functions by their number.
    :param command: number of function
    :return:
    """
    output_list = []
    if command == 1:
        for i in os.listdir(os.getcwd()):
            if os.path.isdir(os.path.join(os.getcwd(), i)):
                output_list.append('→📁 ' + i + '  ')
        for i in os.listdir(os.getcwd()):
            if os.path.isfile(os.path.join(os.getcwd(), i)):
                output_list.append('→📑 ' + i + '  ')
    elif command == 2:
        moveUp()
        output_list = []
    elif command == 3:
        dirName = input('Укажите имя папки: ')
        output_list = moveDown(dirName)
    elif command == 4:
        dirName = input('Введите имя каталога (нажмите [Enter] для подсчета в каталоге '+os.getcwd()+'): ')
        if dirName == '':
            output_list = ['В данном каталоге {} файлов'.format(countFiles(os.getcwd()))]
        else:
            output_list = ['В данном каталоге {} файлов'.format(countFiles(dirName))]
    elif command == 5:
        dirName = input('Введите имя каталога (нажмите [Enter] для подсчета в каталоге '+os.getcwd()+'): ')
        if dirName == '':
            output_list = ['Суммарный объем каталога {} байт'.format(countBytes(os.getcwd()))]
        else:
            output_list = ['Суммарный объем каталога {} байт'.format(countBytes(dirName))]
    elif command == 6:
        fileName = input('Укажите имя файла: ')
        dirName = input('Введите имя каталога (нажмите [Enter] для поиска в каталоге '+os.getcwd()+'): ')
        if dirName == '':
            output_list = findFiles(fileName, os.getcwd())
        else:
            output_list = findFiles(fileName, dirName)
    elif command == 7:
        fileName = input('Укажите имя файла: ')
        output_list = openFile(fileName)
    if command != 8:
        print('\n'*1000)
        doubleOutput(output_list, MENU, distance)

def moveUp():
    """
    Moves to upper directory.
    :return:
    """
    os.chdir('..')

def moveDown(currentDir):
    """
    Moves to lower directory by its name.
    :param currentDir: name of the target directory
    :return: error message if directory not found
    """
    if os.path.isdir(currentDir):
        os.chdir(currentDir)
        return
    return 'Каталога с таким именем не существует'

def countFiles(path):
    """
    Function returns quantity of files and directories in given path.
    :param path: name of given directory
    :return: number of files and directories inside
    :rtype: int
    """
    count = 0
    for file in os.listdir(path):
        full_file = os.path.join(path, file)
        count += 1
        if os.path.isdir(full_file):
            count += countFiles(full_file)
    return count

def countBytes(path):
    """
    Function returns size of given directory in bytes.
    :param path: directory name
    :return: directory size
    :rtype: int
    """
    count = 0
    for file in os.listdir(path):
        full_file = os.path.join(path, file)
        if os.path.isdir(full_file):
            count += countBytes(full_file)
        else:
            count += os.path.getsize(full_file)
    return count

def findFiles(target, path):
    """
    Function returns list of files with target in their name in given directory,
    or error message if files not found.
    :param target: target name
    :param path: given directory name
    :return: list of found files
    :rtype: list
    """
    files_list = []
    for file in os.listdir(path):
        full_file = os.path.join(path, file)
        if os.path.isdir(full_file):
            if findFiles(target, full_file) != ['Файлы с таким именем отсутствуют']:
                files_list += findFiles(target, full_file)
        elif target in file:
                files_list.append('→📑 ' + full_file)
    if files_list == []:
        return ['Файлы с таким именем отсутствуют']
    return [i+'  ' for i in sorted(files_list)]

def openFile(path):
    """
    Function opens file by its name
    :param path: file name
    :return: None
    """
    if os.path.isfile(path):
        os.startfile(path)
        return
    return 'Файл с таким именем отсутствует'

def main():
    """
    Main function loop, prints directory information and menu, lets user choose menu item
    by using acceptCommand() and calls the required function.
    :return:
    """
    print('\n'*1000)
    doubleOutput(distance=distance)
    while True:

        command = acceptCommand()
        runCommand(command)
        if command == 8:
            print('Работа программы завершена.')
            break

main()