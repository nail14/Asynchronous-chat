"""1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и
проверить тип и содержание соответствующих переменных.
Затем с помощью онлайн-конвертера преобразовать строковые представление в формат
 Unicode и также проверить тип и содержимое переменных."""

VAR_1 = 'разработка'
VAR_2 = 'сокет'
VAR_3 = 'декоратор'

STR_LIST = [VAR_1, VAR_2, VAR_3]

for el in STR_LIST:
    print(type(el))
    print(el)

print()

VAR_UNIC_1 = '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'
VAR_UNIC_2 = '\u0441\u043e\u043a\u0435\u0442'
VAR_UNIC_3 = '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'

UNIC_LIST = [VAR_UNIC_1, VAR_UNIC_2, VAR_UNIC_3]

for el in UNIC_LIST:
    print(type(el))
    print(el)


"""2. Каждое из слов «class», «function», «method» записать в байтовом
типе без преобразования в последовательность кодов  (не используя методы
encode и decode) и определить тип, содержимое и длину соответствующих переменных."""


p1 = b'class'
p2 = b'function'
p3 = b'method'

print(type(p1), type(p2), type(p3))
print(p1, p2, p3)


"""3. Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе."""


VAR_1 = 'attribute'
VAR_2 = 'класс'
VAR_3 = 'функция'
VAR_4 = 'type'

VAR_LIST = [VAR_1, VAR_2, VAR_3, VAR_4]

# Вариант 1
for el in VAR_LIST:
    try:
        print(bytes(el, 'ascii'))
    except UnicodeEncodeError:
        print(f'Слово "{el}" невозможно записать в виде байтовой строки')

# Вариант 2
# функция eval() интерпретирует строку как код
for el in VAR_LIST:
    try:
        print('Слово записано в байтовом типе:', eval(f'b"{el}"'))
    except SyntaxError:
        print(
            f'Слово "{el}" невозможно записать в байтовом типе с помощью префикса b')


"""4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из
строкового представления в байтовое и выполнить обратное преобразование
(используя методы encode и decode)."""


for s in ['разработка', 'администрирование', 'protocol', 'standard']:
    p = s.encode('utf-8', 'replace')
    q = p.decode('utf-8')
    print(s, p, q)


"""5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из
байтовового в строковый тип на кириллице."""


import subprocess
import chardet

ARGS = ['ping', 'yandex.ru']
YA_PING = subprocess.Popen(ARGS, stdout=subprocess.PIPE)
for line in YA_PING.stdout:
    result = chardet.detect(line)
    print(result)
    line = line.decode(result['encoding']).encode('utf-8')
    print(line.decode('utf-8'))


"""6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое
программирование», «сокет», «декоратор». Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое."""


with open('test_file.txt', 'w', encoding='utf-8') as t_f:
    t_f.write('сетевое программирование\n')
    t_f.write('сокет\n')

with open('test_file.txt', encoding='utf-8') as t_f:
    for each_line in t_f:
        print(each_line, end="")
