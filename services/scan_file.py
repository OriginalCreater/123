import os
# import time
from openpyxl import load_workbook, utils
from tkinter import filedialog as fd
from modules.search_pusk import one_affel_check
# def path_file():
#     return fd.askopenfilename()


def scan_file(path):
    """Получение пути фаила с информацией 'ИНН'"""
    path = str(path)
    """Создание екземпляра класса для работы с екселем"""
    wb = load_workbook(filename=path)
    """Поиск страници по названию 'Основная'"""
    try:
        book = wb["Основная"]
    except:
        """rename активного листа в 'Основная'"""
        book = wb.active
        book.title = "Основная"
    """Создание списка с столбцами екселя"""
    cpi = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
           "W", "X", "Y", "Z"]
    """Создание списков для необходимых данных"""
    stolb_name = []
    string_range = []


    def scan_stolb_for_inn():
        """Поиск столбца с ИНН"""
        for number_stolb, name_stolb in enumerate(cpi):

            stolb = str(book[f'{name_stolb}1'].value)
            if stolb == "ИНН" or stolb == "Инн" or stolb == "инн":
                stolb_name.append(name_stolb)
                for string_inn in range(1, 1000):
                    """Поиск длинны строк с инн"""
                    max_inn = str(book[f'{name_stolb}{string_inn}'].value)
                    max_inn2 = str(book[f'{name_stolb}{string_inn+1}'].value)
                    max_inn3 = str(book[f'{name_stolb}{string_inn+2}'].value)
                    if max_inn == "None" and max_inn2 == "None" and max_inn3 == "None":
                        string_range.append(string_inn)
                        break
                """Создание столца для результатов проверки"""
                name_rezault_stolb = str(cpi[number_stolb + 1])
                name_reason = str(cpi[number_stolb + 2])


                stolb_name.append(name_rezault_stolb)
                stolb_name.append(name_reason)
                rezault = str(book[f'{name_rezault_stolb}1'].value)
                if rezault == "Результат проверки":
                    """Если найден столбез с резултатами поиск его длинны"""
                    for string_rezault in range(1, 1000):
                        """Поиск длинны колличества результатов для оценки минимального значения"""
                        max_rezault = str(book[f'{name_rezault_stolb}{string_rezault}'].value)
                        if max_rezault == "None":
                            """Запись длинны столбца с результатами"""
                            string_range.append(string_rezault)
                            break
                elif rezault == "None":
                    """Если столбец пуст rename его в 'Результат проверки'"""
                    book[f'{name_rezault_stolb}1'] = f"Результат проверки"
                    string_rezault = 2
                    string_range.append(string_rezault)
                else:
                    """Если чтото иное, создание нового столбца для результатов"""
                    book.insert_cols(number_stolb + 2, 1)
                    book[f'{name_rezault_stolb}1'] = f"Результат проверки"
                    book[f'{name_reason}1'] = f"Причина"
                    string_rezault = 2
                    string_range.append(string_rezault)


    """Начало сканирования фаила на длинну и положение"""
    scan_stolb_for_inn()
    """Сохранение фаила"""
    wb.save(path)
    """Чтение максимальной длинны информации с длинной ИНН"""
    max_range = int(string_range[0])
    """Чтение макисмальной длинны информации с результатами"""
    min_range = int(string_range[1])
    """Сохранение положения столбца с ИНН"""
    inn_stolb = str(stolb_name[0])
    """Сохранение положения столбца с результатами"""
    rezault_stolb = str(stolb_name[1])
    reason_stolb = str(stolb_name[2])
    # print(f"Колличество ИНН: {max_range - 2}")
    # print(f"Колличество проверенных: {min_range - 2}")
    # print(f"ИНН нахоится в столбце: {inn_stolb}")
    # print(f"Результат находится на столбце: {rezault_stolb}")
    inn_list = []
    for i in range(min_range, max_range):
        inn = str(book[f'{inn_stolb}{i}'].value)
        inn = inn.split('.')
        inn = inn[0]
        print(inn)

        inn_list.append(inn)
    return inn_list, rezault_stolb, reason_stolb

def scan_file_affel(path, token):
    """Получение пути фаила с информацией 'ИНН'"""
    path = str(path)
    """Создание екземпляра класса для работы с екселем"""
    wb = load_workbook(filename=path)
    """Поиск страници по названию 'Основная'"""
    try:
        book = wb["Основная"]
    except:
        """rename активного листа в 'Основная'"""
        book = wb.active
        book.title = "Основная"
    """Создание списка с столбцами екселя"""
    cpi = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
           "W", "X", "Y", "Z"]
    """Создание списков для необходимых данных"""
    stolb_name = []
    string_range = []
    stolb_num = []

    def scan_stolb_for_inn():
        """Поиск столбца с ИНН"""
        for number_stolb, name_stolb in enumerate(cpi):

            stolb = str(book[f'{name_stolb}1'].value)
            if stolb == "ИНН" or stolb == "Инн" or stolb == "инн":
                stolb_name.append(name_stolb)
                for string_inn in range(1, 1000):
                    """Поиск длинны строк с инн"""
                    max_inn = str(book[f'{name_stolb}{string_inn}'].value)
                    max_inn2 = str(book[f'{name_stolb}{string_inn+1}'].value)
                    max_inn3 = str(book[f'{name_stolb}{string_inn+2}'].value)
                    if max_inn == "None" and max_inn2 == "None" and max_inn3 == "None":
                        string_range.append(string_inn)
                        wb.save(path)
                        break
                """Создание столца для результатов проверки"""
                name_rezault_stolb = str(cpi[number_stolb + 1])

                stolb_num.append(name_rezault_stolb)
                rezault = str(book[f'{name_rezault_stolb}1'].value)
                if rezault == "Номер":
                    pass
                elif rezault == "None":
                    """Если столбец пуст rename его в 'Результат проверки'"""
                    book[f'{name_rezault_stolb}1'] = f"Номер"
                else:
                    """Если чтото иное, создание нового столбца для результатов"""
                    book.insert_cols(number_stolb + 2, 2)
                    book[f'{name_rezault_stolb}1'] = f"Номер"

    """Начало сканирования фаила на длинну и положение"""
    scan_stolb_for_inn()
    """Сохранение фаила"""
    wb.save(path)
    """Чтение максимальной длинны информации с длинной ИНН"""
    max_range = int(string_range[0])
    """Сохранение положения столбца с ИНН"""
    inn_stolb = str(stolb_name[0])
    num_stolb = str(stolb_num[0])
    inn_list = []
    for i in reversed(range(2, max_range)):
        # inn = str(book[f'{inn_stolb}{i}'].value)
        book.insert_rows(i)
        book[f'{inn_stolb}{i}'] = f"----------"
        wb.save(path)
    max_range_true = []
    for i in range(1, 1000):
        """Поиск длинны строк с инн"""
        max_inn = str(book[f'{inn_stolb}{i}'].value)
        max_inn2 = str(book[f'{inn_stolb}{i + 1}'].value)
        max_inn3 = str(book[f'{inn_stolb}{i + 2}'].value)
        max_inn4 = str(book[f'{inn_stolb}{i + 3}'].value)
        max_inn5 = str(book[f'{inn_stolb}{i + 4}'].value)
        if max_inn == "None" and max_inn2 == "None" and max_inn3 == "None" and max_inn4 == "None" and max_inn5 == "None":
            max_range_true.append(i)
            break
    max = max_range_true[0]
    print(max_range_true[0])
    list_info = []
    for i in range(1, max):
        inn = str(book[f'{inn_stolb}{i}'].value)
        if inn == f"----------":
            pass
        elif inn == "ИНН" or inn == "Инн" or inn == "инн":
            pass
        else:
            list_info.append(inn)
    def index_search(inn):
        for row_index in range(1, book.max_row + 1):  # Начинаем с 1 (первая строка)
            for col_index in range(1, book.max_column + 1):
                cell_value = book.cell(row=row_index, column=col_index).value
                if cell_value == int(inn):  # Сравниваем с искомым значением
                    return row_index  # Возвращаем номер строки
    for i in list_info:
        print(list_info)
        row_index_1 = index_search(i)
        print(i)
        row_index_1 = str(row_index_1)
        inn = row_index_1.split('.')
        row_index_1 = inn[0]

        print(row_index_1)
        inn = str(book[f'{inn_stolb}{row_index_1}'].value)
        inn_list, num_list = one_affel_check(inn, token, row_index_1)
        pos = 0
        for s, a in enumerate(inn_list):
            if a == []:
                pass
            else:
                for i in range(row_index_1, row_index_1 + len(a)):
                    book.insert_rows(i + 1)
                    wb.save(path)
                    book[f'{inn_stolb}{i + 1}'] = f"{a[pos]}"
                    book[f'{num_stolb}{i + 1}'] = f"{int(num_list[s])}"
                    pos += 1
                    wb.save(path)
                else:
                    pos = 0

    return inn_list


# print(scan_file("C:\\Users\\evgeniy\\Desktop\\alve\\uploads\\1213425 (4) (2) (2).xlsx"))