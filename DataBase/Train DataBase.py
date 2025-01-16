import sqlite3

def initialize_database():
    connection = sqlite3.connect(':memory:')
    cursor = connection.cursor()

    # Создание таблицы поездов
    cursor.execute('''
        CREATE TABLE trains (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            train_number TEXT NOT NULL,
            departure_station TEXT NOT NULL,
            arrival_station TEXT NOT NULL,
            departure_time TEXT NOT NULL,
            arrival_time TEXT NOT NULL
        )
    ''')

    # Создание таблицы остановок
    cursor.execute('''
        CREATE TABLE stops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            train_id INTEGER NOT NULL,
            stop_name TEXT NOT NULL,
            stop_time TEXT NOT NULL,
            FOREIGN KEY (train_id) REFERENCES trains(id)
        )
    ''')

    # Создание таблицы цен
    cursor.execute('''
        CREATE TABLE prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            train_id INTEGER NOT NULL,
            class TEXT NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (train_id) REFERENCES trains(id)
        )
    ''')

    # Создание таблицы времени в пути
    cursor.execute('''
        CREATE TABLE travel_times (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            train_id INTEGER NOT NULL,
            duration TEXT NOT NULL,
            FOREIGN KEY (train_id) REFERENCES trains(id)
        )
    ''')

    # Создание таблицы проданных мест
    cursor.execute('''
        CREATE TABLE sold_seats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            train_id INTEGER NOT NULL,
            seat_number TEXT NOT NULL,
            passenger_name TEXT NOT NULL,
            FOREIGN KEY (train_id) REFERENCES trains(id)
        )
    ''')

    connection.commit()
    return connection

def add_train(connection, train_number, departure_station, arrival_station, departure_time, arrival_time):
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO trains (train_number, departure_station, arrival_station, departure_time, arrival_time)
        VALUES (?, ?, ?, ?, ?)
    ''', (train_number, departure_station, arrival_station, departure_time, arrival_time))
    connection.commit()

def add_stop(connection, train_id, stop_name, stop_time):
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO stops (train_id, stop_name, stop_time)
        VALUES (?, ?, ?)
    ''', (train_id, stop_name, stop_time))
    connection.commit()

def add_price(connection, train_id, class_type, price):
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO prices (train_id, class, price)
        VALUES (?, ?, ?)
    ''', (train_id, class_type, price))
    connection.commit()

def add_travel_time(connection, train_id, duration):
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO travel_times (train_id, duration)
        VALUES (?, ?)
    ''', (train_id, duration))
    connection.commit()

def add_sold_seat(connection, train_id, seat_number, passenger_name):
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO sold_seats (train_id, seat_number, passenger_name)
        VALUES (?, ?, ?)
    ''', (train_id, seat_number, passenger_name))
    connection.commit()

def view_all_data(connection):
    cursor = connection.cursor()
    print("\nТаблица поездов:")
    for row in cursor.execute('SELECT * FROM trains'):
        print(row)

    print("\nТаблица остановок:")
    for row in cursor.execute('SELECT * FROM stops'):
        print(row)

    print("\nТаблица цен:")
    for row in cursor.execute('SELECT * FROM prices'):
        print(row)

    print("\nТаблица времени в пути:")
    for row in cursor.execute('SELECT * FROM travel_times'):
        print(row)

    print("\nТаблица проданных мест:")
    for row in cursor.execute('SELECT * FROM sold_seats'):
        print(row)

def main():
    connection = initialize_database()

    while True:
        print("\nМеню:")
        print("1. Добавить поезд")
        print("2. Добавить остановку")
        print("3. Добавить цену")
        print("4. Добавить время в пути")
        print("5. Добавить проданное место")
        print("6. Показать всю базу данных")
        print("0. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            train_number = input("Номер поезда: ")
            departure_station = input("Станция отправления: ")
            arrival_station = input("Станция прибытия: ")
            departure_time = input("Время отправления: ")
            arrival_time = input("Время прибытия: ")
            add_train(connection, train_number, departure_station, arrival_station, departure_time, arrival_time)

        elif choice == "2":
            train_id = int(input("ID поезда: "))
            stop_name = input("Название остановки: ")
            stop_time = input("Время остановки: ")
            add_stop(connection, train_id, stop_name, stop_time)

        elif choice == "3":
            train_id = int(input("ID поезда: "))
            class_type = input("Класс: ")
            price = float(input("Цена: "))
            add_price(connection, train_id, class_type, price)

        elif choice == "4":
            train_id = int(input("ID поезда: "))
            duration = input("Длительность поездки: ")
            add_travel_time(connection, train_id, duration)

        elif choice == "5":
            train_id = int(input("ID поезда: "))
            seat_number = input("Номер места: ")
            passenger_name = input("Имя пассажира: ")
            add_sold_seat(connection, train_id, seat_number, passenger_name)

        elif choice == "6":
            view_all_data(connection)

        elif choice == "0":
            break
        else:
            print("Неверный выбор, попробуйте снова.")

if __name__ == "__main__":
    main()