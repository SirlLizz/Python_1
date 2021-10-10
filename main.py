import zipfile
import os
import hashlib
import re
import requests

# Задание №1

directory_to_extract_to = 'C:\\Users\\Ilya\\Desktop\\Pric_prog\\1_laba'     # директория извлечения файлов архива
arch_file = 'C:\\Users\\Ilya\\Desktop\\Pric_prog\\1_laba\\tiff-4.2.0_lab1.zip'      # путь к архиву
path = '\\arhiv'

# Открытие zip-архива
test_zip = zipfile.ZipFile(arch_file)

# Просмотр содержимого архива
test_zip_files = test_zip.namelist()
print(test_zip_files)

directory_to_extract_to += path
# Создание новой директории
try:
    os.mkdir(directory_to_extract_to)
except OSError:
    print("Создать директорию не удалось")
else:
    print("Успешно создана директория")

# Извлечение всех файлов из архива в директорию
test_zip.extractall(directory_to_extract_to)

# Завершение работы с архивом
test_zip.close()

# Задание №2.1
# Получить список файлов (полный путь) формата txt, находящихся в directory_to_extract_to.
# Сохранить полученный список в txt_files

txt_files = []
for r, d, f in os.walk(directory_to_extract_to):
    for i in f:
        tmp = os.path.join(r, i)
        if ".txt" in i:
            txt_files.append(tmp)
        # txt_files.append(tmp)
print("Файлы с расширением txt")
for i in txt_files:
    print(i)
print('\n')

# Задание №2.2
# Получить значения MD5 хеша для найденных файлов и вывести полученные данные на экран.

tmp = []
for file in txt_files:
    data = open(file, "rb")
    content = data.read()
    tmp.append(hashlib.md5(content).hexdigest())
    data.close()
print("Хэши файлов")
for i in tmp:
    print(i)
print('\n')

# Задание №3

target_hash = "4636f9ae9fef12ebd56cd39586d33cfb"
target_file = ''  # полный путь к искомому файлу
target_file_data = ''  # содержимое искомого файла

# Найти файл MD5 хеш которого равен target_hash в directory_to_extract_to

for r, d, f in os.walk(directory_to_extract_to):
    for i in f:
        tmp = os.path.join(r, i)
        data = open(tmp, "rb")
        content = data.read()
        if hashlib.md5(content).hexdigest() == target_hash:
            target_file = r + "\\" + i
            target_file_data = content

# Отобразить полный путь к искомому файлу и его содержимое на экране

print("Файл с указанным хэшем")
print(target_file)
print(target_file_data)

# Задание №4
# Ниже представлен фрагмент кода парсинга HTML страницы с помощью регулярных выражений.
# Возможно выполнение этого задания иным способом (например, с помощью сторонних модулей).

r = requests.get(target_file_data)
result_dct = {}  # словарь для записи содержимого таблицы

counter = 0
# Получение списка строк таблицы
lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)
for line in lines:
    # извлечение заголовков таблицы
    if counter == 0:
        # Удаление тегов
        headers = re.sub(..., ..., line)
        # Извлечение списка заголовков
        headers = re.findall(..., headers)

        # TODO

    # Удаление тегов
    temp = re.sub(..., ';', line)
    # Значения в таблице, заключенные в скобках, не учитывать. Для этого удалить скобки и символы между ними.
    temp = ...
    # Замена последовательности символов ';' на одиночный символ
    temp = ...
    # Удаление символа ';' в начале и в конце строки

    # TODO

    # Разбитие строки на подстроки
    tmp_split = ...

    # Извлечение и обработка (удаление "лишних" символов) данных из первого столбца
    country_name = tmp_split[0]

    # TODO

    # Извлечение данных из оставшихся столбцов. Данные из этих столбцов должны иметь числовое значение (прочерк можно заменить на -1).
    # Некоторые строки содержат пробелы в виде символа '\xa0'.
    col1_val = ...
    col2_val = ...
    col3_val = ...
    col4_val = ...

    # Запись извлеченных данных в словарь
    result_dct[country_name] = ...
    result_dct[country_name][...] = int(col1_val)
    result_dct[country_name][...] = int(col2_val)
    result_dct[country_name][...] = int(col3_val)
    result_dct[country_name][...] = int(col4_val)

    counter += 1

    # Задание №5
    # Запись данных из полученного словаря в файл
    output = open('data.csv', 'w')
    for key in result_dct.keys():

    # TODO

    output.close()

    # Задание №6
    # Вывод данных на экран для указанного первичного ключа (первый столбец таблицы)

    target_country = input("Введите название страны: ")

    # TODO