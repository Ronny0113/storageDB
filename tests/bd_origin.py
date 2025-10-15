import sqlite3
import os


def import_colors(path):
    with open(f"{path}", mode='r') as ral_table:
        colors_list = []
        for line in ral_table:
            splitted = line.split(';')
            color_list = (splitted[0], splitted[1], splitted[2], splitted[3].replace('\n', ''))
            colors_list.append(color_list)
        return colors_list


def create_database(bd_name):
    create_sheets_table = '''CREATE TABLE IF NOT EXISTS sheets (
                             sheet_id INTEGER PRIMARY KEY,
                             color_ral INTEGER,
                             size TEXT,
                             quantity INTEGER,
                             cut_quantity INTEGER DEFAULT 0,
                             FOREIGN KEY (color_ral) REFERENCES colors(color_ral_id)
                         )'''

    create_colors_table = '''CREATE TABLE IF NOT EXISTS colors (
                             color_ral_id INTEGER PRIMARY KEY,
                             rgb TEXT,
                             hex TEXT,
                             color_name TEXT
                         )'''

    insert_colors_data = '''INSERT INTO colors (color_ral_id, rgb, hex, color_name) VALUES (?, ?, ?, ?)'''

    if not os.path.isfile(f"{bd_name}.db"):
        with sqlite3.connect(f"{bd_name}.db") as conn:
            conn.execute(create_sheets_table)
            conn.execute(create_colors_table)
            colors = import_colors("ral.txt")
            for color in colors:
                conn.execute(insert_colors_data, color)
            conn.commit()
            print("База данных успешно создана!")
    else:
        print("База данных с таким названием уже существует!")


def add_sheet(bd_name, color, size, quantity):
    if quantity <= 0:
        print("Введите положительное число!")
        return
    with sqlite3.connect(f"{bd_name}") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        insert_new_sheet = f"INSERT INTO sheets (color_ral, size, quantity) VALUES ({color}, '{size}', {quantity})"
        check = conn.execute(f"SELECT * FROM sheets WHERE color_ral={color} AND size = '{size}'").fetchall()
        if not check:
            check_ral = conn.execute(f"SELECT * FROM colors WHERE color_ral_id={color}").fetchall()
            if not check_ral:
                print("Неверный RAL")
                return
            else:
                conn.execute(insert_new_sheet)
        else:
            conn.execute(f"UPDATE sheets SET quantity={quantity + check[0][3]} WHERE sheet_id={check[0][0]}")
        conn.commit()
        if quantity == 1:
            print("Лист успешно добавлен")
        else:
            print("Листы успешно добавлены")


def delete_sheet(bd_name, color, size, quantity):
    if quantity < 0:
        print("Введите положительное число!")
        return
    with sqlite3.connect(f"{bd_name}") as conn:
        check = conn.execute(f"SELECT * FROM sheets WHERE color_ral={color} AND size='{size}'").fetchall()
        if not check:
            print("Нет листов с такими параметрами")
            return
        else:
            if quantity == check[0][3]:
                conn.execute(f"DELETE FROM sheets WHERE color_ral={color} AND size ='{size}'")
                print(f"Успешно удалено следующее количество листов: {quantity}")
            elif quantity > check[0][3]:
                print("Невозможно удалить листов больше, чем у вас есть")
                return
            else:
                conn.execute(f"UPDATE sheets SET quantity={check[0][3] - quantity} WHERE sheet_id={check[0][0]}")
                print(f"Успешно удалено следующее количество листов: {quantity}")
        conn.commit()


def cut_sheet(bd_name, sheet, new_size):
    with sqlite3.connect(f"{bd_name}") as conn:
        check = conn.execute(f"SELECT * FROM sheets WHERE sheet_id={sheet}").fetchall()
        if not check:
            print("Нет листа с таким ID")
            return
        else:
            if check[0][3] == 1:
                conn.execute(f"DELETE FROM sheets WHERE sheet_id={sheet}")
                check2 = conn.execute(f"SELECT * FROM sheets WHERE color_ral={check[0][1]} AND size='{new_size}'").\
                    fetchall()
                if not check2:
                    conn.execute(f"INSERT INTO sheets (color_ral, size, quantity, is_cutted) VALUES ({check[0][1]},"
                                 f"'{new_size}', 1, 1)")
                    print("Обрезка выполнена")
                else:
                    conn.execute(f"UPDATE sheets SET quantity={check2[0][3] + 1} WHERE sheet_id={check2[0][0]}")
                    print("Обрезка выполнена")
            if check[0][3] > 1:
                conn.execute(f"UPDATE sheets SET quantity={check[0][3] - 1} WHERE sheet_id={check[0][0]}")
                check2 = conn.execute(f"SELECT * FROM sheets WHERE color_ral={check[0][1]} AND size='{new_size}'").\
                    fetchall()
                if not check2:
                    conn.execute(f"INSERT INTO sheets (color_ral, size, quantity, is_cutted) VALUES ({check[0][1]},"
                                 f"'{new_size}', 1, 1)")
                    print("Обрезка выполнена")
                else:
                    conn.execute(f"UPDATE sheets SET quantity={check2[0][3] + 1} WHERE sheet_id={check2[0][0]}")
                    print("Обрезка выполнена")
                print("")
            conn.commit()


'''def show_table(bd_name, table_name):
    with sqlite3.connect(f"{bd_name}") as conn:
        info = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
        for i in info:
            print(i[1], end=' ')
        print('')
        table = conn.execute(f"SELECT * FROM {table_name}").fetchall()
        for j in table:
            print(j)'''


def show_table(bd_name, table_name):
    with sqlite3.connect(f"{bd_name}") as conn:
        info = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
        table = conn.execute(f"SELECT * FROM {table_name}").fetchall()

        column_widths = []
        for i, col in enumerate(info):
            column_widths.append(max(len(col[1]), max(len(str(row[i])) for row in table)))

        for i, col in enumerate(info):
            print(f"{col[1]:<{column_widths[i]}} |", end=' ')
        print('')

        for row in table:
            for j, item in enumerate(row):
                print(f"{str(item):<{column_widths[j]}} |", end=' ')
            print('')


#cut_sheet('test.db', 2, '100x300')
show_table('test.db', 'sheets')
#create_database("test")
#add_sheet("test.db", 6000, "20x50", 10)
#delete_sheet("test.db", 6000, '20x50', 3000)
