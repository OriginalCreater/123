from openpyxl import load_workbook



def record(path: str, pos_resault,pos_reason,pos, inn, reason, answer):
    position_stold = pos_resault
    position_reason = pos_reason
    position_string = pos+2
    """ path = fr"UPLOAD_FOLDER"/"filename" """
    file = load_workbook(filename=path)
    book = file["Основная"]
    if answer == True:
        answer = "Свободен"
    elif answer == False:
        answer = "Занят"
    book[f'{position_stold}{position_string}'] = f"{answer}"
    book[f'{position_reason}{position_string}'] = f"{reason}"
    print(f"{answer} | Причина:{reason} | {inn}")
    file.save(path)