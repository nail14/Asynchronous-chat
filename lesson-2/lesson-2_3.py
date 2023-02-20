"""
3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий
сохранение данных в файле YAML-формата. Для этого:
a. Подготовить данные для записи в виде словаря, в котором первому ключу
соответствует список, второму — целое число, третьему — вложенный словарь, где
значение каждого ключа — это целое число с юникод-символом, отсутствующим в
кодировке ASCII (например, €);
b. Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
При этом обеспечить стилизацию файла с помощью параметра default_flow_style, а
также установить возможность работы с юникодом: allow_unicode = True;
c. Реализовать считывание данных из созданного файла и проверить, совпадают ли они
с исходными.


"""

import yaml

key_1 = ['Windows', 'Android', 'Linux', 'IOS']
key_2 = 1234
key_3 = {
    'a': '€',
    'b': 'Æ',
    'c': 'ɷ'
}
data_to_yaml = {'key_1': key_1, 'key_2': key_2, 'key3': key_3}
yaml_str = yaml.dump(data_to_yaml, allow_unicode=True, default_flow_style=False)
# print(yaml_str)
# пишем строку в файл file.yaml
with open('file.yaml', 'w', encoding="UTF-8") as f_n:
    f_n.write(yaml_str)
# читаем из файла
with open('file.yaml', 'r', encoding="UTF-8") as f_r:
    data_from_yaml = yaml.load(f_r)
print("Read from file: ", data_from_yaml)
if data_from_yaml == data_to_yaml:
    print("Equal")
else:
    print("Different")