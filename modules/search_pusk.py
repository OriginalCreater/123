import time

from flask import jsonify
# sys.path.insert(1, os.path.join(sys.path[0], "../../services"))
from services.getInn import get_id_companies, get_id_affel, get_id_affel_mail, get_id_affel_site, get_id_affel_name
from services.getStatusCompanies import getStatusCompanies, checkStatusCompanies, get_number_affel, get_mail_affel, get_site_affel,get_name_affel
from services.getDynamic import getDinamic
from services.getSecondaryFilterData import getOMP
from services.recResults import record
from services.getDocs import getDoc
def check_companies(list_inn, pos_resault,pos_reason, path, token):
    results_uuid = []
    results_inn = []
    for string, inn in enumerate(list_inn):
        if inn == "----------":
            continue
        # print(f"=============={inn}======ххх=========")
        if not inn:
            return jsonify({"error": "Missing 'inn' parameter"}), 400
        list_uuid = get_id_companies(inn, token)
        print(list_uuid)
        # if list_uuid is []:
        #     record(path, pos_resault, string, inn, "J", True)
        # else:
        for uuid in list_uuid:
            time.sleep(1.5)
            company_result = {"inn": inn, "result": True}  # Start with a default True result
            # Check each condition and update the result accordingly

            if not checkStatusCompanies(getStatusCompanies(uuid, token)):
                company_result["result"] = False
                company_result["reason"] = "Статус"
            elif not getDinamic(uuid, token):
                company_result["result"] = False
                company_result["reason"] = "Динамика"
            elif not getOMP(uuid, token):
                company_result["result"] = False
                company_result["reason"] = "ОМП"
            results_uuid.append(company_result)  # Append the result for this company
        for info in results_uuid:
            if info["inn"] == inn:
                results_inn.append(info)
        if results_inn == []:
            record(path, pos_resault,pos_reason, string, inn, "ККА-0", True)
        else:
            for value in results_inn:
                if value["result"] == False:
                    record(path, pos_resault,pos_reason, string, value["inn"], value["reason"], value["result"])
                    break
            else:
                record(path, pos_resault, pos_reason, string, results_inn[-1]["inn"], "Не выявлено", True)
        results_inn = []
    return jsonify(results_uuid)  # Return results as JSON
def one_inn_check(inn,token):
    results_uuid = []
    results_inn = []
    list_uuid = get_id_companies(inn, token)
    print(list_uuid)
    # if list_uuid is []:
    #     record(path, pos_resault, string, inn, "J", True)
    # else:
    for uuid in list_uuid:
        time.sleep(1.5)
        company_result = {"inn": inn, "result": True}  # Start with a default True result
        # Check each condition and update the result accordingly

        if not checkStatusCompanies(getStatusCompanies(uuid, token)):
            company_result["result"] = False
            company_result["reason"] = "Статус"
        elif not getDinamic(uuid, token):
            company_result["result"] = False
            company_result["reason"] = "Динамика"
        elif not getOMP(uuid, token):
            company_result["result"] = False
            company_result["reason"] = "ОМП"
        results_uuid.append(company_result)  # Append the result for this company
    for info in results_uuid:
        if info["inn"] == inn:
            results_inn.append(info)
    if results_inn == []:
         value, reason, result = inn, "ККА-0", True
    else:
        for value in results_inn:
            if value["result"] == False:
                value, reason, result = value["inn"], value["reason"], value["result"]
                break
        else:
            value, reason, result = results_inn[-1]["inn"], "Не выявлено", True
    return value, reason, result
def search_docs(number,token):
    info = getDoc(number, token)
    if info == "3":
        res = "Месячный"
        print(res)
        return res
    elif info == "2":
        res = "Еженедельный"
        print(res)
        return res
def one_affel_check(inn, token, pos, phone):
    print(inn)
    print(f"Телефоны - {phone}")
    """Удаление лишнего из номеров ексель"""
    ch = ['-', '(', ' ', ")"]

    for i in ch:
        phone = phone.replace(i, "")

    print(phone)
    """Разделение номеров ексель на елименты списка"""
    info_phone = phone.split(',')
    print(info_phone)
    """Берем елимент списка и получаем длинну строки если = 12 ок если 11 меняем первый спимвол на +7 иначе удаляем 
    номер"""
    list_uuid = get_id_companies(inn, token)
    time.sleep(2)
    number_list = []
    main_info_num = []
    main_info_inn = []
    for i in list_uuid:
        number = get_number_affel(i, token)
        if number == None:
            pass
        else:
            number_list.append(number)
    if number_list == []:
        pass
    else:
        li = [i for n, i in enumerate(number_list) if i not in number_list[:n]]
        for i in li:
            main_info_num.append(i)
            list_inn = get_id_affel(str(i), token)
            if len(list_inn) >= 10:
                main_info_inn = False
                main_info_num = False
                return main_info_inn, main_info_num
            else:
                li_i = [i for n, i in enumerate(list_inn) if i not in list_inn[:n]]
                try:
                    li_i.remove(str(inn))
                except ValueError:
                    pass
                for i in li_i:
                    if i == "":
                        li_i.remove("")
                main_info_inn.append(li_i)
    # print(main_info_inn)
    # print(main_info_num)
    return main_info_inn, main_info_num
def one_affel_email(inn, token, pos):
    # print(inn)
    list_uuid = get_id_companies(inn, token)
    time.sleep(2)
    email_list = []
    main_info_mail = []
    main_info_inn = []
    for i in list_uuid:
        mail = get_mail_affel(i, token)
        mail = str(mail).split(", ")
        for i in mail:
            if i != "None":
                email_list.append(i)
    email_list = set(email_list)
    if email_list == set():
        email_list = []
    for email in email_list:
        list_inn = get_id_affel_mail(i, token)
        list_inn = set(list_inn)
        if "" in list_inn:
            list_inn.remove("")
        if inn in list_inn:
            list_inn.remove(inn)
        if list_inn == set():
            list_inn = []
        main_info_mail.append(email)
        main_info_inn.append(list_inn)
        # print(f"Почта = {email}")
        # print(f"Связанные с ней ИНН = {list_inn}")
    inn_info_list = []
    for i in main_info_inn:
        for o in i:
            j = []
            j.append(o)
            inn_info_list.append(j)
    # print(f"ИНН = {inn_info_list}")
    # print(f"Емеил = {main_info_mail}")
    return inn_info_list, main_info_mail

def one_affel_site(inn, token, pos):
    # print(inn)
    list_uuid = get_id_companies(inn, token)
    time.sleep(2)
    a = []
    f = []
    g = []
    site_list = []
    main_info_site = []
    main_info_inn = []
    for i in list_uuid:
        site = get_site_affel(i, token)
        if site == None:
            pass
        else:
            a.append(site)
        if a == []:
            pass
        else:
            [site_list.append(val) for val in a if val not in site_list]
            f.append(site_list)
    [g.append(val) for val in f if val not in g]
    # print(g)
    for i in g:
        for n in i:
            main_info_site.append(n)
    for i in main_info_site:
        list_inn = get_id_affel_site(i, token)
        for i in range(len(list_inn)):
            if inn in list_inn:
                list_inn.remove(inn)
        if list_inn == []:
            pass
        else:
            main_info_inn.append(list_inn)
    # print(main_info_site)
    # print(main_info_inn)
    return main_info_inn, main_info_site
def one_affel_name(inn, token, pos):
    # print(inn)
    list_uuid = get_id_companies(inn, token)
    time.sleep(2)
    a = []
    f = []
    g = []
    name_list = []
    main_info_name = []
    main_info_inn = []
    for i in list_uuid:
        name = get_name_affel(i, token)
        if name == None:
            pass
        else:
            a.append(name)
        if a == []:
            pass
        else:
            [name_list.append(val) for val in a if val not in name_list]
            f.append(name_list)
    [g.append(val) for val in f if val not in g]
    # print(g)
    for i in g:
        for n in i:
            main_info_name.append(n)
    for i in main_info_name:
        list_inn = get_id_affel_name(i, token)
        for i in range(len(list_inn)):
            if inn in list_inn:
                list_inn.remove(inn)
        if list_inn == []:
            pass
        else:
            main_info_inn.append(list_inn)
    return main_info_inn, main_info_name



    #     mail = str(mail).split(", ")
    #     for i in mail:
    #         if i != "None":
    #             site_list.append(i)
    # email_list = set(site_list)
    # if email_list == set():
    #     email_list = []
    # for email in email_list:
    #     list_inn = get_id_affel_mail(i, token)
    #     list_inn = set(list_inn)
    #     if "" in list_inn:
    #         list_inn.remove("")
    #     if inn in list_inn:
    #         list_inn.remove(inn)
    #     if list_inn == set():
    #         list_inn = []
    #     main_info_site.append(email)
    #     main_info_inn.append(list_inn)
    #     # print(f"Почта = {email}")
    #     # print(f"Связанные с ней ИНН = {list_inn}")
    # inn_info_list = []
    # for i in main_info_inn:
    #     for o in i:
    #         j = []
    #         j.append(o)
    #         inn_info_list.append(j)
    # print(f"ИНН = {inn_info_list}")
    # print(f"Емеил = {main_info_site}")
    # return inn_info_list, main_info_site
    #     if mail == None:
    #         pass
    #     else:
    #         email_list.append(mail)
    # if email_list == []:
    #     pass
    # else:
    #     li = [i for n, i in enumerate(email_list) if i not in email_list[:n]]
    #     for i in li:
    #         main_info_mail.append(i)
    #         list_inn = get_id_affel(str(i), token)
    #         li_i = [i for n, i in enumerate(list_inn) if i not in list_inn[:n]]
    #         li_i.remove(str(inn))
    #         for i in li_i:
    #             if i == "":
    #                 li_i.remove("")
    #         main_info_inn.append(li_i)
    # print(main_info_inn)
    # print(main_info_mail)
    # return main_info_inn, main_info_mail

