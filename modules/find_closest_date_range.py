from datetime import datetime

def find_closest_date_range(date_list, target_date_str, date_format='%d.%m.%Y', preferred_uuid=None):
    try:
        target_date = datetime.strptime(target_date_str, date_format)
    except ValueError:
        raise ValueError(f"Введенная дата '{target_date_str}' не соответствует формату '{date_format}'")

    if not date_list:
        return None

    valid_ranges = []  # Записи, действующие на target_date
    closest_range = None
    min_distance_seconds = float('inf')

    for item in date_list:
        active_from = datetime.strptime(item['activeFrom'], date_format)
        active_to = None
        if 'activeTo' in item and item['activeTo']:
            try:
                active_to = datetime.strptime(item['activeTo'], date_format)
            except ValueError:
                print(f"Некорректная дата 'activeTo' в записи {item['uuid']}: {item['activeTo']}")
                continue

        # Проверяем, попадает ли target_date в диапазон или запись открыта и активна
        is_valid = False
        if active_to:
            if active_from <= target_date <= active_to:
                is_valid = True
        else:
            if active_from <= target_date:
                is_valid = True  # Открытый диапазон, действующий после activeFrom

        if is_valid:
            valid_ranges.append(item)
        else:
            # Вычисляем расстояние до ближайшей даты диапазона
            distance = abs(target_date - active_from) if active_from > target_date else abs(target_date - active_to) if active_to else float('inf')
            distance_seconds = distance.total_seconds()
            if distance_seconds < min_distance_seconds:
                min_distance_seconds = distance_seconds
                closest_range = item

    # Обрабатываем действующие диапазоны
    if valid_ranges:
        # Сначала ищем по preferred_uuid
        if preferred_uuid:
            for item in valid_ranges:
                if item['uuid'] == preferred_uuid and 'price' in item:
                    return item['price']
        
        # Затем ищем любой с price
        for item in reversed(valid_ranges):
            if 'price' in item:
                return item['price']
        return None  # Если ни у одной действующей записи нет price

    # Если нет действующих диапазонов, возвращаем ближайший с price
    if closest_range and 'price' in closest_range:
        return closest_range['price']
    
    return None