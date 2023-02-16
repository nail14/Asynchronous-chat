"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку
определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый
«отчетный» файл в формате CSV. Для этого:
a. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с
данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения
каждого параметра поместить в соответствующий список. Должно получиться четыре
списка — например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же
функции создать главный список для хранения данных отчета — например, main_data
— и поместить в него названия столбцов отчета в виде списка: «Изготовитель
системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data (также для
каждого файла);

"""

import re
import csv
from typing import List, Any


def get_data(files):
    templates = ['Изготовитель системы*:', 'Название ОС*:', 'Код продукта*:', 'Тип системы*:']
    for curr_file in files:
        i = 0
        with open(curr_file) as file_i:
            newrow = []
            for line in file_i:
                line = line.strip()
                for template in templates:
                    match = re.match(template, line)
                    if match:
                        if template == templates[0]:
                            os_prod_list.append(line[match.end():].strip())
                        elif template == templates[1]:
                            os_name_list.append(line[match.end():].strip())
                        elif template == templates[2]:
                            os_code_list.append(line[match.end():].strip())
                        elif template == templates[3]:
                            os_type_list.append(line[match.end():].strip())
            newrow.append(os_prod_list[i])
            newrow.append(os_name_list[i])
            newrow.append(os_code_list[i])
            newrow.append(os_type_list[i])
            main_data.append(newrow)
            i = i+1
            file_i.close()

"""b. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой
функции реализовать получение данных через вызов функции get_data(), а также
сохранение подготовленных данных в соответствующий CSV-файл;"""

def write_to_csv(new_csv_file: object):
    file_writer = csv.writer(new_csv_file, delimiter=',')
    for row in main_data:
        file_writer.writerow(row)


os_prod_list: List[Any] = []
os_name_list: List[Any] = []
os_code_list: List[Any] = []
os_type_list: List[Any] = []
main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]
input_files = ['info_1.txt', 'info_2.txt', 'info_3.txt']
get_data(input_files)
print(os_prod_list, '\n', os_name_list, '\n', os_code_list, '\n', os_type_list, '\n')
print(main_data)


"""c. Реализовать считывание данных из созданного файла и проверить, совпадают ли они
с исходными.
"""

with open('main_data.csv', 'w') as f_n:
    write_to_csv(f_n)
    f_n.close()