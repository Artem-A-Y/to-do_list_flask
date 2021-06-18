# to-do_list_flask
Простой to-do list

1. установить виртуальное окружение. Пример: 
>> python3 -m venv venv
2. Нужно сообщить системе, что вы хотите использовать виртуальное окружение, активируя его. Чтобы активировать новое виртуальное окружение нужно:
>> source venv/bin/activate
Если вы используете cmd (окно командной строки Microsoft Windows), команда активации немного отличается: 
>> venv\Scripts\activate
3. >> pip install -r requirements
4. Установив переменную среды FLASK_APP:
>> export FLASK_APP=todo.py
5. Применить изменения в базе данных:
>> flask db upgrade
6. >> flask run
