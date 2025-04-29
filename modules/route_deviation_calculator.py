import pandas as pd
from datetime import datetime
from services.priceEarth import priceEarth
from services.priceAir import priceAir
from services.locality import city
from modules.find_closest_date_range import find_closest_date_range


def route_deviation_calculator(token,df,result_df1):
    result_df1['Дата первого отклонения'] = pd.to_datetime(
    result_df1['Дата первого отклонения'], 
    format='mixed'
).dt.tz_localize(None)

    # Инициализируем combined_df из result_df1
    combined_df = result_df1.copy()

    # Добавляем только 'Расчетный вес округленный' из df
    df_grouped = df.groupby('№ заказа').agg({
        'Расчетный вес округленный': 'first'
    }).reset_index()

    combined_df = pd.merge(combined_df, df_grouped, on='№ заказа', how='left')

    # Обрабатываем все заказы
    for index, row in combined_df.iterrows():
        order_id = row['№ заказа']
        target_date = row['Дата первого отклонения']
        transport_type = row['Вид тр-та (факт)']  # Получаем вид транспорта
        
        # Если дата отсутствует, используем значение по умолчанию
        if pd.isna(target_date):
            target_date = '01.01.2025'
        else:
            target_date = target_date.strftime('%d.%m.%Y')  # Форматируем для priceEarth/priceAir
        
        # Получаем коды городов из result_df1
        start_city = row['Начальный город']
        end_city = row['Конечный город']
        
        # Проверяем, что города не None
        if pd.isna(start_city) or pd.isna(end_city):
            print(f"Order {order_id}: Skipping due to missing city (Start: {start_city}, End: {end_city})")
            combined_df.loc[index, 'price'] = 0.0
            continue
        
        start_city_code = city(token, start_city)
        end_city_code = city(token, end_city)
        
        # Проверяем, что коды городов получены
        if not start_city_code or not end_city_code:
            print(f"Order {order_id}: Skipping due to invalid city codes (Start: {start_city_code}, End: {end_city_code})")
            combined_df.loc[index, 'price'] = 0.0
            continue
        
        # Выбираем функцию в зависимости от вида транспорта
        if transport_type == 'Земля (Магистральные перевозки)':
            date_list = priceEarth(token, start_city_code, end_city_code, target_date)
        elif transport_type == 'Воздух (Авиационные перевозки)':
            date_list = priceAir(token, start_city_code, end_city_code, target_date)
        else:
            print(f"Order {order_id}: Unknown transport type '{transport_type}', skipping price calculation")
            combined_df.loc[index, 'price'] = 0.0
            continue
        
        # Находим ближайший диапазон цен
        result_data = find_closest_date_range(date_list, target_date)
        if result_data is not None:
            combined_df.loc[index, 'price'] = result_data
        else:
            print(f"Order {order_id}: No price found for date {target_date}")
            combined_df.loc[index, 'price'] = 0.0

    # Функция для извлечения числового значения из price
    def extract_price(price_str):
        if pd.isna(price_str) or not isinstance(price_str, str):
            return 0.0
        try:
            return float(price_str.split()[0])  # Извлекаем число перед 'руб/кг'
        except (AttributeError, ValueError):
            return 0.0

    # Преобразуем price в число и вычисляем итоговую сумму
    combined_df['price'] = combined_df['price'].apply(extract_price)
    combined_df['Итоговая сумма'] = (combined_df['Сумма операций (по условиям)'] - 
                                    (combined_df['Расчетный вес округленный'].fillna(0) * combined_df['price']))

    # Убеждаемся, что '№ заказа' остается Int64
    combined_df['№ заказа'] = combined_df['№ заказа'].astype('Int64')

    # Сохраняем таблицу в новый Excel-файл
    output_file = 'output_table.xlsx'
    combined_df.to_excel(output_file, index=False)

    # Выводим результат
    print("Итоговый combined_df:")
    print(combined_df)
    print("\nТипы данных столбцов:")
    print(combined_df.dtypes)
    print(f"Таблица сохранена в файл: {output_file}")