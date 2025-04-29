import pandas as pd

def extract_city_from_office(office_str):
    if pd.isna(office_str) or not isinstance(office_str, str):
        return None
    parts = office_str.split(', ')
    return parts[2] if len(parts) >= 3 else None  # Город на третьей позиции

def find_extra_steps(group):
    planned_route = list(zip(group['Код офиса Откуда (план)'], group['Код офиса Куда (план)']))
    actual_route = list(zip(group['Код офиса Откуда (факт)'], group['Код офиса Куда (факт)']))
    
    extra_steps = []
    total_sum = 0
    first_deviation_date = None
    first_extra_from_city = None  # Город первого отклонения
    last_extra_to_city = None    # Город последнего отклонения
    first_transport_type = None  # Вид транспорта для первого отклонения
    target_types = ["5.2 Перевозка до города-получателя/транзита", 
                    "15.2 Складская обработка (транзит)", 
                    "15.1 Складская обработка",
                    "5.2.1 Перевозка до города-получателя/транзита (многоместные)"]
    
    # Находим индексы всех лишних звеньев
    extra_indices = []
    for i, step in enumerate(actual_route):
        if step not in planned_route:
            extra_steps.append(step)
            extra_indices.append(i)
            # Сохраняем данные первого отклонения
            if first_deviation_date is None and 'Дата операции' in group.columns:
                first_deviation_date = group.iloc[i]['Дата операции']
                first_extra_from_city = extract_city_from_office(group.iloc[i]['Откуда (факт)'])  # Извлекаем город
                # Сохраняем вид транспорта для первого отклонения
                if 'Вид тр-та (факт)' in group.columns:
                    first_transport_type = group.iloc[i]['Вид тр-та (факт)']
            # Обновляем город последнего отклонения
            last_extra_to_city = extract_city_from_office(group.iloc[i]['Куда (факт)'])  # Извлекаем город
    
    # Если есть лишние звенья
    if extra_indices:
        # Берем диапазон от первого до последнего лишнего звена
        start_index = extra_indices[0]
        end_index = extra_indices[-1]
        
        # Суммируем все операции в target_types между первым и последним лишним звеном
        for i in range(start_index, end_index + 1):
            if group.iloc[i]['Тип оаерации'] in target_types:  # Предполагается опечатка, должно быть "Тип операции"
                sum_value = str(group.iloc[i]['Сумма операции, руб']).replace(',', '.')
                total_sum += float(sum_value)
    
    return extra_steps, total_sum, first_deviation_date, first_extra_from_city, last_extra_to_city, first_transport_type
