from flask import Flask, request, jsonify
import re
import mysql.connector
import datetime
import bcrypt
from datetime import datetime, timedelta
import mysql.connector.pooling
import json
app = Flask(__name__)
import time
import os
from datetime import datetime
import time
from threading import Thread


# Replace with your database configuration
# mydb = mysql.connector.connect(
#     host="ideal-web.site",
#     user="admin_alexunderlag",
#     password="OG+J(0@T{E[uakY@",
#     database="admin_python"
# )


dbconfig = {
    "host": "localhost",
    "user": "admin_alexunderlag",
    "password": "OG+J(0@T{E[uakY@",
    "database": "admin_python",
    "pool_name": "mypool",
    "pool_size": 5
}

pool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
JSON_FILE_PATH = "users.json"
JSON_FILE_PATH_SHT = "sht_data.json"




def check_duration():
    conn = pool.get_connection()
    mycursor = conn.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM piramid WHERE id = 1")
    piramid = mycursor.fetchone()
    
    if not piramid['start_date']:
        # Если start_time не установлено, ничего не делаем.
        return
    
    elapsed_time = (datetime.now() - piramid['start_date']).seconds

    if elapsed_time >= piramid['duration']:
        # Выполняем нужное действие, например, обнуление баланса
        mycursor.execute("UPDATE piramid SET balance = 0, participants = 0, start_date = NOW(), lastuser = DEFAULT, end_date = DATE_ADD(NOW(), INTERVAL duration SECOND) WHERE id = 1")
        conn.commit()
    
    mycursor.close()
    conn.close()
    
def background_task():
    while True:
        check_duration()
        time.sleep(5)

def get_remaining_seconds_for_piramid():
    conn = pool.get_connection()
    mycursor = conn.cursor(dictionary=True)
    
    mycursor.execute("SELECT * FROM piramid WHERE id = 1")
    piramid = mycursor.fetchone()
    
    mycursor.close()
    conn.close()

    if not piramid['end_date']:
        # Если end_date не установлено, вернем 0
        return 0

    # Разница между временем окончания и текущим временем
    remaining_time = piramid['end_date'] - datetime.now()

    # Возврат разницы в секундах
    return remaining_time.total_seconds()
def get_remaining_seconds_for_piramid2():
    conn = pool.get_connection()
    mycursor = conn.cursor(dictionary=True)
    
    mycursor.execute("SELECT * FROM piramid WHERE id = 2")
    piramid = mycursor.fetchone()
    
    mycursor.close()
    conn.close()

    if not piramid['end_date']:
        # Если end_date не установлено, вернем 0
        return 0

    # Разница между временем окончания и текущим временем
    remaining_time = piramid['end_date'] - datetime.now()

    # Возврат разницы в секундах
    return remaining_time.total_seconds()

def get_elapsed_seconds_from_total_duration():
    conn = pool.get_connection()
    mycursor = conn.cursor(dictionary=True)
    
    mycursor.execute("SELECT * FROM piramid WHERE id = 1")
    piramid = mycursor.fetchone()
    
    mycursor.close()
    conn.close()

    if not piramid['end_date'] or not piramid['start_date']:
        # Если end_date или start_date не установлены, вернем 0
        return 0

    # Общая продолжительность пирамиды в секундах
    total_duration = (piramid['end_date'] - piramid['start_date']).total_seconds()

    # Разница между временем окончания и текущим временем
    remaining_time = (piramid['end_date'] - datetime.now()).total_seconds()

    # Возврат разницы между общим временем и оставшимся временем
    return total_duration - remaining_time
def get_elapsed_seconds_from_total_duration2():
    conn = pool.get_connection()
    mycursor = conn.cursor(dictionary=True)
    
    mycursor.execute("SELECT * FROM piramid WHERE id = 2")
    piramid = mycursor.fetchone()
    
    mycursor.close()
    conn.close()

    if not piramid['end_date'] or not piramid['start_date']:
        # Если end_date или start_date не установлены, вернем 0
        return 0

    # Общая продолжительность пирамиды в секундах
    total_duration = (piramid['end_date'] - piramid['start_date']).total_seconds()

    # Разница между временем окончания и текущим временем
    remaining_time = (piramid['end_date'] - datetime.now()).total_seconds()

    # Возврат разницы между общим временем и оставшимся временем
    return total_duration - remaining_time
@app.route('/register', methods=['POST'])
def register():
    current_date = datetime.now()
    conn = pool.get_connection()
    data = request.json
    login = data.get('login')
    email = data.get('email')
    password = data.get('password')
    password_dub = data.get('password_dub')
    fname = data.get('fname')
    lname = data.get('lname')
    city = data.get('city')
    mobile = data.get('mobile')
    birthdate = data.get('birthdate')
    promocode = data.get('promocode')
    hide_email = data.get('hide_email', 0)
    hide_phone = data.get('hide_phone', 0)
    hide_city = data.get('hide_city', 0)
    # Email validation
    if not is_valid_email(email):
        return jsonify({'status': 'error', 'message': 'Некоректный Email'}), 400

    # Password match validation
    if password != password_dub:
        return jsonify({'status': 'error', 'message': 'Пароли не совпадают'}), 400
    if not login:
        return jsonify({'status': 'error', 'message': 'Логин не может быть пустым'}), 400

    if len(login) < 3 or len(login) > 16:
        return jsonify({'status': 'error', 'message': 'Логин должен содержать от 3 до 16 символов'}), 400

    if not login.isascii():
        return jsonify({'status': 'error', 'message': 'Логин может содержать только английские буквы'}), 400

    if not login.isalpha():
        return jsonify({'status': 'error', 'message': 'Логин не может содержать цифры или специальные символы'}), 400

    # Password validation
    if not password:
        return jsonify({'status': 'error', 'message': 'Пароль не может быть пустым'}), 400

    if len(password) < 3:
        return jsonify({'status': 'error', 'message': 'Пароль должен содержать минимум 3 символа'}), 400
    
    if len(mobile) != 12 or not mobile.startswith("+7") or not mobile[1:].isdigit():
        return jsonify({'status': 'error', 'message': 'Некорректный номер телефона'}), 400
    
    mycursor = conn.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM user WHERE login = %s", (login,))
    myresult = mycursor.fetchone()


    # Проверка существования email
    mycursor.execute("SELECT * FROM user WHERE email = %s", (email,))
    email_result = mycursor.fetchone()
    if email_result is not None:
        return jsonify({'status': 'error', 'message': 'Email уже существует'}), 400

    # Проверка существования номера телефона
    mycursor.execute("SELECT * FROM user WHERE mobile = %s", (mobile,))
    mobile_result = mycursor.fetchone()
    if mobile_result is not None:
        return jsonify({'status': 'error', 'message': 'Телефон уже существует'}), 400
    
    if myresult is None:
        # Хэширование пароля
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        mycursor.execute(
            """
            INSERT INTO user(login, password, fname, lname, city, mobile, balance, email, date_register, birthdate, promocode, hide_email, hide_phone, hide_city) 
            VALUES (%s, %s, %s, %s, %s, %s, 0, %s, %s, %s, %s, %s, %s, %s)
            """,
            (login, hashed_password, fname, lname, city, mobile, email, current_date, birthdate, promocode, hide_email, hide_phone, hide_city)
        )
        conn.commit()
        mycursor.close()
        conn.close()
        update_json_file()
        update_menu_file()
        return jsonify({'status': 'success', 'message': 'Регистрация успешна'})
    else:
        return jsonify({'status': 'error', 'message': 'Пользователь уже существует'}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    login = data.get('login')
    password = data.get('password')
    conn = pool.get_connection()
    mycursor = conn.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM user WHERE login = %s", (login,))
    myresult = mycursor.fetchone()
    mycursor.close()
    conn.close()
    if myresult is None:
        return jsonify({'status': 'error', 'message': 'Неверное имя пользователя или пароль'}), 400
    else:
        # Проверка хэшированного пароля
        if bcrypt.checkpw(password.encode('utf-8'), myresult['password'].encode('utf-8')):
            return jsonify({'status': 'success', 'message': 'Авторизация успешна', 'user': myresult})
        else:
            return jsonify({'status': 'error', 'message': 'Неверное имя пользователя или пароль'}), 400
    
def is_valid_email(email):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(email_regex, email) is not None

@app.route('/deposit', methods=['POST'])
def deposit():
    data = request.json
    login = data.get('login')
    balances = int(data.get('amount'))
    conn = pool.get_connection()
    mycursor = conn.cursor(dictionary=True)
    
    # Проверяем баланс пользователя
    mycursor.execute("SELECT * FROM user where login = %s", (login,))
    user = mycursor.fetchone()

    mycursor.execute("SELECT * FROM piramid WHERE id = 1")
    piramid = mycursor.fetchone()
    min = int(piramid['minshag'] )
    stav = int(piramid['balance'] )
    minstavka = min + stav
    lastuser = piramid['lastuser']
    balance2 = balances / 2

    if user:
        user_balance = int(user['balance'])
        
        if balances > user_balance:
            return jsonify({'status': 'error', 'message': 'У Вас меньше денег, чем вы хотите положить'})
        elif minstavka > balances:
            return jsonify({'status': 'error', 'message': 'Вы хотите положить меньше, минимальной ставки'})
        else:
            
            # Обновление баланса в БД
            mycursor.execute("UPDATE user SET balance = balance - %s WHERE login = %s", (balances , login))
            mycursor.execute("UPDATE piramid SET balance = balance + %s,minstavka = balance + minshag, participants = participants + 1, start_date = NOW() WHERE id = 1", (balances,))
            current_balance = int(piramid['balance'])
            mycursor.execute("UPDATE user SET balance = balance + %s + %s WHERE login = %s;", (current_balance, balance2, lastuser))
            mycursor.execute("UPDATE piramid SET lastuser = %s WHERE id = %s;", (login, 1))
            conn.commit()
            mycursor.close()
            conn.close()
            return jsonify({'status': 'success', 'message': 'Пополнение успешно'})
    else:
        return jsonify({'status': 'error', 'message': 'Пользователь не найден'})

@app.route('/deposit2', methods=['POST'])
def deposit2():
    data = request.json
    login = data.get('login')
    balances = int(data.get('amount'))
    conn = pool.get_connection()
    mycursor = conn.cursor(dictionary=True)
    
    
    # Проверяем баланс пользователя
    mycursor.execute("SELECT * FROM user where login = %s", (login,))
    user = mycursor.fetchone()

    mycursor.execute("SELECT * FROM piramid WHERE id = 2")
    piramid = mycursor.fetchone()
    min = int(piramid['minshag'] )
    stav = int(piramid['balance'] )
    minstavka = min + stav
    lastuser  = piramid['lastuser']
    balance2 =  balances / 2

    if user:
        user_balance = int(user['balance'])
        
        if balances > user_balance:
            return jsonify({'status': 'error', 'message': 'У Вас меньше денег, чем вы хотите положить'})
        elif minstavka > balances:
            return jsonify({'status': 'error', 'message': 'Вы хотите положить меньше, минимальной ставки'})
        else:
            # Обновление баланса в БД
            mycursor.execute("UPDATE user SET balance = balance - %s WHERE login = %s", ( balances , login))
            mycursor.execute("UPDATE piramid SET balance = balance + %s, participants = participants + 1 WHERE id = 2", (balances,))
            current_balance = int(piramid['balance'])
            mycursor.execute("UPDATE user SET balance = balance + %s + %s WHERE login = %s;", (current_balance, balance2, lastuser))
            mycursor.execute("UPDATE piramid SET lastuser = %s WHERE id = %s;", (login, 1))
            conn.commit()
            update_pyramid()
            mycursor.close()
            conn.close()
            return jsonify({'status': 'success', 'message': 'Пополнение успешно'})
    else:
        return jsonify({'status': 'error', 'message': 'Пользователь не найден'})


def update_pyramid():
    conn = pool.get_connection()
    mycursor = conn.cursor(dictionary=True)

    mycursor.execute("SELECT * FROM piramid WHERE id = 1")
    piramid = mycursor.fetchone()
    start_date = piramid['start_date']
    end_date = piramid['end_date']

    # Проверка, прошел ли день с момента последнего пополнения пирамиды
    current_date = datetime.datetime.now().date()
    if current_date >= end_date:
        # Сдвиг даты на следующий день и аннулирование баланса
        new_end_date = end_date + datetime.timedelta(days=1)
        # Обновление записи пирамиды в базе данных
        mycursor.execute("UPDATE piramid SET end_date = %s WHERE id = 1",(new_end_date,))
        conn.commit()
        mycursor.close()
        conn.close()
@app.route('/logout', methods=['POST'])
def logout():
    # Ваш код для выполнения операций выхода из системы
    # Например, удаление данных аутентификации, сброс сеанса и т.д.
    
    return jsonify({'message': 'Выход выполнен успешно'})


@app.route('/get_user_info', methods=['POST'])
def get_user_info():
    data = request.json
    login = data.get('lname')
    conn = pool.get_connection()
    mycursor = conn.cursor(dictionary=True)

    # Запрос в БД
    mycursor.execute("SELECT * FROM user WHERE lname = %s;", (login,))
    print(login)
    user = mycursor.fetchone()
    mycursor.close()
    conn.close()
    
    if user is None:
        return jsonify({'message': 'Пользователь не найден'}), 404

    # Hide user data based on the values in hide_email, hide_phone, and hide_city
    if user['hide_email'] == 1:
        user['email'] = 'скрыто'
    if user['hide_phone'] == 1:
        user['mobile'] = 'скрыто'
    if user['hide_city'] == 1:
        user['city'] = 'скрыто'

    # Remove fields not to be sent in the response, such as hide_email, hide_phone, hide_city
    del user['hide_email']
    del user['hide_phone']
    del user['hide_city']

    return jsonify(user)
    

@app.route('/get_piramid_data', methods=['GET'])
def get_piramid_data():
    conn = pool.get_connection()
    mycursor = conn.cursor(dictionary=True)

    def calculate_progress(piramid_data):
        if piramid_data['start_date'] and piramid_data['duration']:
            elapsed_time = (datetime.now() - piramid_data['start_date']).seconds
            return (elapsed_time / piramid_data['duration'])   # возвращает процент выполнения
        return 0  # если нет начального времени или продолжительности, возвращаем 0%
    def calculate_progress(piramid_data2):
        if piramid_data2['start_date'] and piramid_data2['duration']:
            elapsed_time = (datetime.now() - piramid_data2['start_date']).seconds
            return (elapsed_time / piramid_data2['duration'])   # возвращает процент выполнения
        return 0  # если нет начального времени или продолжительности, возвращаем 0%
    
    # Получение данных для пирамиды с ID 1
    mycursor.execute("SELECT * FROM piramid WHERE id = 1;")
    piramid_data = mycursor.fetchone()
    piramid_data['seconds_left'] = get_remaining_seconds_for_piramid()
    piramid_data['ost_proc'] = get_elapsed_seconds_from_total_duration()
    piramid_data['progress'] = calculate_progress(piramid_data)

    # Получение данных для пирамиды с ID 2
    mycursor.execute("SELECT * FROM piramid WHERE id = 2;")
    piramid_data2 = mycursor.fetchone()
    piramid_data2['seconds_left'] = get_remaining_seconds_for_piramid2()
    piramid_data2['ost_proc'] = get_elapsed_seconds_from_total_duration2()
    piramid_data2['progress'] = calculate_progress(piramid_data2)

    mycursor.close()
    conn.close()

    # Возврат данных для обеих пирамид в одном ответе
    return jsonify(
        piramid_data=piramid_data,
        piramid_data2=piramid_data2,
    )

@app.route('/menu_sht', methods=['GET'])
def update_sht():
    # Проверка существования файла и времени последнего обновления
    if not os.path.exists(JSON_FILE_PATH_SHT) or time.time() - os.path.getmtime(JSON_FILE_PATH_SHT) > 1800:
        update_menu_file()
    
    # Возвращение данных из JSON-файла
    with open(JSON_FILE_PATH_SHT, 'r') as f:
        data = json.load(f)
        return jsonify(data)
    
@app.route('/advertup', methods=['GET'])
def update_newstoday():
    # mydb.reconnect()
    # mycursor = mydb.cursor(dictionary=True)
    # mycursor.execute("SELECT MAX(ID) FROM user;")
    # follow = mycursor.fetchone()
    
    newstoday = 'Добро пожаловать на закрытое бето тестирование. Спасибо что Вы с намии)))'  # Замените эту дату на вашу начальную дату
    return jsonify({"newstoday": newstoday})


@app.route('/update_balance', methods=['POST'])
def update_balance():
    data = request.json
    login = data.get('login')
    balance = data.get('balance')
    conn = pool.get_connection()
    mycursor = conn.cursor(dictionary=True)

    # Обновление баланса в БД
    mycursor.execute("UPDATE user SET balance = balance + %s WHERE login = %s;", (balance, login))
    conn.commit()

    # Получение обновленного баланса
    mycursor.execute("SELECT balance FROM user WHERE login = %s;", (login,))
    new_balance = mycursor.fetchone().get('balance')
    mycursor.close()
    conn.close()
    return jsonify({'message': 'Баланс успешно пополнен', 'new_balance': new_balance})

@app.route('/get_all_users', methods=['GET'])
def get_all_users():
    # Проверка существования файла и времени последнего обновления
    if not os.path.exists(JSON_FILE_PATH) or time.time() - os.path.getmtime(JSON_FILE_PATH) > 3600:
        update_json_file()

    # Возвращение данных из JSON-файла
    with open(JSON_FILE_PATH, 'r') as f:
        data = json.load(f)
        return jsonify(data)
    
def update_json_file():
    try:
        conn = pool.get_connection()
        mycursor = conn.cursor(dictionary=True)
        mycursor.execute("SELECT fname, lname, date_register, balance FROM user;")
        users = mycursor.fetchall()

        for user in users:
            if user["date_register"]:
                user["date_register"] = user["date_register"].strftime('%Y-%m-%d')
            else:
                user["date_register"] = "Неизвестно"
        mycursor.close()
        conn.close()

        # Сохранение в JSON
        with open(JSON_FILE_PATH, 'w') as f:
            json.dump({'Users': users}, f)
        print(f"Файл {JSON_FILE_PATH} успешно обновлен.")
        
    except Exception as e:
        print(f"Ошибка при обновлении файла {JSON_FILE_PATH}:", e)
def update_menu_file():
    conn = pool.get_connection()
    mycursor = conn.cursor(dictionary=True)
    mycursor.execute("SELECT MAX(ID) FROM user;")
    follow = mycursor.fetchone()
    mycursor.execute("SELECT MAX(ID) FROM piramid;")
    piramidkol = mycursor.fetchone()

    start_date = datetime(2023, 7, 1)
    today = datetime.now()
    days_passed = (today - start_date).days
    mycursor.close()
    conn.close()

    data = {
        'max_user_id': follow["MAX(ID)"],
        'max_piramid_id': piramidkol["MAX(ID)"],
        'tdays': days_passed
    }

    # Сохранение в JSON
    with open(JSON_FILE_PATH_SHT, 'w') as f:
        json.dump(data, f)

if __name__ == '__main__':
    t = Thread(target=background_task)
    t.start()
    app.run(debug=True, host='77.73.68.140')