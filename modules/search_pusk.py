import time

from flask import jsonify
# sys.path.insert(1, os.path.join(sys.path[0], "../../services"))
from services.getInn import get_id_companies, get_id_affel
from services.getStatusCompanies import getStatusCompanies, checkStatusCompanies, get_number_affel
from services.getDynamic import getDinamic
from services.getSecondaryFilterData import getOMP
from services.recResults import record

def check_companies(list_inn, pos_resault,pos_reason, path, token):
    results_uuid = []
    results_inn = []
    for string, inn in enumerate(list_inn):

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

def one_affel_check(inn, token, pos):
    print(inn)
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
            li_i = [i for n, i in enumerate(list_inn) if i not in list_inn[:n]]
            li_i.remove(str(inn))
            for i in li_i:
                if i == "":
                    li_i.remove("")
            main_info_inn.append(li_i)
    print(main_info_inn)
    print(main_info_num)
    return main_info_inn, main_info_num

