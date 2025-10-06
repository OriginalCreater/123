from time import sleep
from services.getInn import get_id_companies
from services.login import refresh_token, exchange_code
from services.getStatusCompanies import getStatusCompanies, checkStatusCompanies
from services.getDynamic import getDinamic
from services.getSecondaryFilterData import getOMP
from modules.search_pusk import check_companies,one_inn_check
from flask import Flask, jsonify, render_template, request, current_app, send_from_directory, redirect, url_for, make_response, send_file
from services.scan_file import scan_file, scan_file_affel, duble_opti, scan_file_docs, ovk_skan
import os
import pandas as pd
from localStoragePy import localStoragePy
from modules.custom_round import custom_round
from modules.find_extra_step import find_extra_steps, extract_city_from_office
from modules.route_deviation_calculator import route_deviation_calculator


app = Flask(__name__)
localStorage = localStoragePy('your-app-namespace', 'your-storage-backend')
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
name = []
info = {}
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/auth')
def auth():
    return render_template('login.html')
@app.route('/ct')
def ct():
    return render_template('control_task.html')
@app.route('/wh')
def wh():
    return render_template('warehouse.html')
@app.route('/affel')
def affel():
    return render_template("affel.html")
@app.route('/docs')
def docs():
    return render_template("docs.html")

@app.route('/menu')
def menu():
    return render_template('cdek_menu.html')
def save_in_cookie(token):
    response = make_response(render_template("login.html"))
    TOKEN = token
    response.set_cookie('access_token', 'YOUR_ACCESS_TOKEN')
    response.set_cookie('refresh_token', 'TOKEN')
@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form.get('username')
    password = request.form.get('password')
    response_data = refresh_token(username, password)
    # print(response_data)
    access_token = request.cookies.get('token')
    # if response_data["token"] != access_token:
    #     info['username'] = username
    #     info['password'] = password
    #     return redirect(url_for('code_input'))
    try:
        if response_data["codeTtl"] == 300:
            info['username'] = username
            info['password'] = password
            return redirect(url_for('code_input'))
    except KeyError:
        if response_data["token"]:
            info['token'] = response_data['token']
            save_in_cookie(response_data["token"])
            return redirect(url_for('menu'))
        elif response_data["token"] == access_token:
            info['token'] = response_data['token']
            save_in_cookie(response_data["token"])
            return redirect(url_for('menu'))



@app.route('/code_input')
def code_input():
    return render_template('code_input.html')

@app.route('/submit_code', methods=['GET', 'POST'])
def submit_code():
    code = request.form.get('code')
    info['code'] = code
    response_data = exchange_code(info['username'], info["password"], info['code'])
    print(response_data)
    if response_data["token"] == None:
        # Запись логина и пароля в словарь
        return redirect(url_for('login'))
    else:
        info['token'] = response_data['token']
        response = make_response(render_template("login.html"))
        TOKEN = response_data["token"]
        response.set_cookie('access_token', 'YOUR_ACCESS_TOKEN')
        response.set_cookie('refresh_token', 'TOKEN')
        return redirect(url_for('menu'))




@app.route('/pusk')
def pusk():
    return render_template('index_pusk.html')

@app.route('/pusk_one', methods=["GET", 'POST'])  # Корневой маршрут для отображения формы и результата
def pusk_one():
    result = None  # Инициализируем переменную для результата
    message = None
    token = info["token"]
    if request.method == 'POST':
        inn = request.form['inn']  # Получаем ИНН из формы
        value, message, result = one_inn_check(inn, token)
        if result == True:
            message = f"Свободен - {message}"
        elif result == False:
            message = f"Занят - {message}"
    return render_template('index_pusk_one.html', result=result, message=message)  # Передаем результат в шаблон HTML


@app.route('/upload', methods=["GET",'POST'])
def upload():
    if request.method == 'POST':
        """Загрузка фаила в дерикторию uploads"""
        uploaded_files = request.files.getlist("file")
        uploaded_file = uploaded_files[0]
        filename = uploaded_file.filename
        name.append(filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(file_path)
        return redirect("/scan_html")


@app.route("/scan_html", methods=["GET",'POST'])
def scan_html():
    return render_template("index_scan.html")

@app.route('/scan', methods=['GET'])
def scan():
    if request.method == "GET":
        filename = name[-1]
        path = fr"{UPLOAD_FOLDER}/{filename}"
        list_inn, pos_resault, pos_reason = scan_file(path)
        token = info['token']
        check_companies(list_inn, pos_resault, pos_reason, path, token)
        # return jsonify(list_inn)
        return redirect("/uploaded_html")

@app.route("/uploaded_html")
def uploaded_html():
    return render_template("index_end.html")

@app.route('/uploaded',  methods=['GET'])
def uploaded():
    if request.method == 'GET':
        filename = name[-1]
        uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
        return send_from_directory(uploads, filename)





@app.route("/affel_search", methods = ["POST"])
def affel_search():
    files = request.files.getlist("file")
    uploaded_files = request.files.getlist("file")
    uploaded_file = uploaded_files[0]
    filename = uploaded_file.filename
    name.append(filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    uploaded_file.save(file_path)
    return redirect("/scan_html_affel")
@app.route("/docs_search", methods = ["POST"])
def docs_search():
    files = request.files.getlist("file")
    uploaded_files = request.files.getlist("file")
    uploaded_file = uploaded_files[0]
    filename = uploaded_file.filename
    name.append(filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    uploaded_file.save(file_path)
    return redirect("/scan_html_docs")
@app.route("/upload_affel_pusk", methods = ['POST'])
def upload_affel_pusk():
    files = request.files.getlist("file")
    uploaded_files = request.files.getlist("file")
    uploaded_file = uploaded_files[0]
    filename = uploaded_file.filename
    name.append(filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    uploaded_file.save(file_path)
    return redirect("/scan_html_affel_pusk")
@app.route("/scan_html_affel_pusk", methods=["GET",'POST'])
def scan_html_affel_pusk():
    return render_template("index_scan_affel_pusk.html")
# @app.route("/scan_html_affel", methods=["GET",'POST'])
# def scan_html_affel():
#     return render_template("index_scan_affel.html")

@app.route("/pusk_affel", methods = ["GET",'POST'])
def pusk_affel():
    return render_template('pusk_affel_index.html')
@app.route("/scan_html_affel", methods=["GET",'POST'])
def scan_html_affel():
    return render_template("index_scan_affel.html")
@app.route("/scan_html_docs", methods=["GET",'POST'])
def scan_html_docs():
    return render_template("index_scan_docs.html")
@app.route('/scan_affel_pusk', methods=['GET'])
def scan_affel_pusk():
    if request.method == "GET":
        filename = name[-1]
        path = fr"{UPLOAD_FOLDER}/{filename}"
        token = info['token']
        duble_opti(path)
        affel = scan_file_affel(path, token)
        duble_opti(path)
        list_inn, pos_resault, pos_reason = scan_file(path)
        token = info['token']
        check_companies(list_inn, pos_resault, pos_reason, path, token)
        # check_companies(list_inn, pos_resault, pos_reason, path, token)
        # return jsonify(list_inn)
        # return redirect("/uploaded_html")
        return(redirect("/uploaded_html"))
@app.route('/scan_affel', methods=['GET'])
def scan_affel():
    if request.method == "GET":
        filename = name[-1]
        path = fr"{UPLOAD_FOLDER}/{filename}"
        token = info['token']
        list_inn = scan_file_affel(path, token)

        # check_companies(list_inn, pos_resault, pos_reason, path, token)
        # return jsonify(list_inn)
        # return redirect("/uploaded_html")
        return(redirect("/uploaded_html"))
@app.route('/scan_docs', methods=['GET'])
def scan_docs():
    if request.method == "GET":
        filename = name[-1]
        path = fr"{UPLOAD_FOLDER}/{filename}"
        token = info['token']
        list_docs = scan_file_docs(path, token)

        # check_companies(list_inn, pos_resault, pos_reason, path, token)
        # return jsonify(list_inn)
        # return redirect("/uploaded_html")
        return(redirect("/uploaded_html"))


"""Анализ транспортных схем"""
@app.route('/ovk')
def ovk():
    return render_template('ovk.html')


# @app.route("/ovk_html", methods=["GET",'POST'])
# def ovk_html():
#
@app.route('/process', methods=["GET",'POST'])
def process():
    TOKEN = info["token"]
    files = request.files.getlist("file")
    uploaded_files = request.files.getlist("file")
    uploaded_file = uploaded_files[0]
    filename = uploaded_file.filename
    name.append(filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    uploaded_file.save(file_path)
    print(file_path)
    return render_template("ovk_html.html")
        # return redirect("/ovk_html.html")


@app.route('/end_ovk', methods=["GET",'POST'])
def end_ovk():
        TOKEN = info["token"]
        file_path = f"{UPLOAD_FOLDER}/{name[-1]}"
        ovk = ovk_skan(file_path, TOKEN)
        return redirect("/uploaded_html")

        # # Читаем Excel-файл в DataFrame
        # df = pd.read_csv(str(file_path), sep=';')
        #
        # # Шаг 1: Применяем custom_round для округления веса
        # df['Расчетный вес округленный'] = df.apply(custom_round, axis=1)
        # print("After custom_round:")
        # print(df.info())
        #
        # # Шаг 2: Вычисляем result_df1 с помощью find_extra_steps
        # results = []
        # for order_id, group in df.groupby('№ заказа'):
        #     extra_steps, total_sum, first_deviation_date, first_extra_from_city, last_extra_to_city, first_transport_type = find_extra_steps(group)
        #     if extra_steps:
        #         results.append({
        #             '№ заказа': order_id,
        #             'Лишние звенья': extra_steps,
        #             'Сумма операций (по условиям)': total_sum,
        #             'Дата первого отклонения': first_deviation_date,
        #             'Начальный город': first_extra_from_city,
        #             'Конечный город': last_extra_to_city,
        #             'Вид тр-та (факт)': first_transport_type
        #         })
        # result_df1 = pd.DataFrame(results)
        # print("Result_df1:")
        # print(result_df1)
        #
        # # Шаг 3: Выполняем route_deviation_calculator
        # route_deviation_calculator(TOKEN, df, result_df1)
        #
        # # Возвращаем сгенерированный файл
        # return send_file('output_table.xlsx', as_attachment=True, download_name='output_table.xlsx')
if __name__ == '__main__':
    print("ok")
    app.run(debug=True, host="0.0.0.0", port=5000)
# @app.route('/get_token', methods=['POST'])
# def get_token(): # обновление токена по коду с смс
#     data = request.get_json()
#     login = data.get("login")
#     password = data.get("password")
#     code = data.get("code")
#
#     response_data = exchange_code(login, password, code)
#     print(response_data)
#     if 'token' in response_data:
#         return jsonify({"status": "success", "token": response_data['token']})
#     else:
#         return jsonify({"status": "error", "message": "Не удалось получить токен", "data": response_data})
# @app.route('/send_sms', methods=['POST'])
# def send_sms(): #ообновление токена
#     data = request.get_json()
#     login = data.get("login")
#     password = data.get("password")
#
#     # Отправляем запрос для входа и ожидания SMS
#     response_data = refresh_token(login, password)
#     print(response_data.text)
#     if 'token' in response_data:
#         return print(localStorage.getItem("tokenDisplay"))
#         # return jsonify({"status": "success", "message": "SMS отправлено", "data": response_data})
#     else:
#         print(2)
#         return jsonify({"status": "error", "message": "Не удалось отправить SMS", "data": response_data})
