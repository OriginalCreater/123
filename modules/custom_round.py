import numpy as np

def custom_round(row):
    weight = row['Расчетный вес, кг']
    gm_count_str = str(row['Кол-во ГМ'])
    gm_count = float(gm_count_str.replace(',', '.'))
    
    
    if gm_count == 1:
        if weight > 1:
            
            return np.ceil(weight)
        elif weight < 0.5:
            
            return 0.5
        else:
            
            return 1.0
    
    else:
        
        return np.ceil(weight * 10) / 10