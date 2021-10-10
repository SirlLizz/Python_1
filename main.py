import zipfile
import os
import hashlib
import re
import requests
import csv

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
        headers = re.sub('<.*?>', ' ', line)
        # Извлечение списка заголовков
        headers = re.findall(r'Заболели|Умерли|Вылечились|Активные случаи', headers)
        print(headers)
    else:
        # Удаление тегов
        # Значения в таблице, заключенные в скобках, не учитывать.
        # Для этого удалить скобки и символы между ними.
        # Замена последовательности символов ';' на одиночный символ
        # Удаление символа ';' в начале и в конце строки
        temp = re.sub('<.*?>', ';', line)
        temp = re.sub("\(.*?\)", '', temp)
        temp = re.sub(';+', ';', temp)
        temp = temp[1: len(temp) - 1]
        temp = re.sub('\s(?=\d)', '', temp)
        temp = re.sub('(?<=\d)\s', '', temp)
        temp = re.sub('(?<=0)\*', '', temp)
        temp = re.sub('_', '-1', temp)

        # Разбитие строки на подстроки
        tmp_split = temp.split(';')
        if len(tmp_split) == 6:
            tmp_split.pop(0)

        # Извлечение и обработка (удаление "лишних" символов) данных из первого столбца
        country_name = tmp_split[0]
        country_name = re.sub('.*\s\s', '', country_name)

        # Извлечение данных из оставшихся столбцов. Данные из этих столбцов должны иметь числовое значение
        # (прочерк можно заменить на -1).
        # Некоторые строки содержат пробелы в виде символа '\xa0'.
        col1_val = tmp_split[1]
        col2_val = tmp_split[2]
        col3_val = tmp_split[3]
        col4_val = tmp_split[4]

        # Запись извлеченных данных в словарь
        result_dct[country_name] = [0, 0, 0, 0]
        result_dct[country_name][0] = int(col1_val)
        result_dct[country_name][1] = int(col2_val)
        result_dct[country_name][2] = int(col3_val)
        result_dct[country_name][3] = int(col4_val)

    counter += 1

# Задание №5
# Запись данных из полученного словаря в файл
output = open('data.csv', 'w')
w = csv.writer(output, delimiter=";")
w.writerow(headers)
for key in result_dct.keys():
    w.writerow([key, result_dct[key][0], result_dct[key][1], result_dct[key][2], result_dct[key][3]])
output.close()

# Задание №6
# Вывод данных на экран для указанного первичного ключа (первый столбец таблицы)

target_country = input("Введите название страны: ")
print(result_dct[target_country])

