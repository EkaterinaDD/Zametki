import time
import json

def save(zametki):
    with open("savedZametki.json", "w", encoding="utf-8") as doc:
        doc.write(json.dumps(zametki, ensure_ascii=False))

def load():
    try:
        print("<---Zametki--->")
        with open("savedZametki.json", "r", encoding="utf-8") as doc:
            zametki = json.load(doc)
        print("Загрузка заметок завершена\n")
        save(zametki)
        return zametki
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Ошибка при загрузке файла JSON. Файл поврежден/имеет неверный формат.")
        return {}

def showAll(zametki):
    if(zametki):
        print("Все заметки:")
        for id, data in zametki.items():
            print(f"№ {data.get('id', 'N/A')}; {data.get('titleZametka', 'N/A')}; Дата: {data.get('currentDate', 'N/A')}")
        zametka_id = input("Открыть свою заметку? Введите ID. Хотите назад? Введите \"no\": ")
        if zametka_id.lower() != "no":
            show_zametka_body(zametki, zametka_id)
    else:
        print("Заметок нет.")

def showDate(zametki):
    if(zametki):
        print("Введите диапазон дат, чтобы отфильтровать заметки:")
        start_date = input("Введите начальную дату (формат: ДД-ММ-ГГГГ): ")
        end_date = input("Введите конечную дату (формат: ДД-ММ-ГГГГ): ")

        try:
            start_time = time.strptime(start_date, "%d-%m-%Y")
            end_date = time.strptime(end_date, "%d-%m-%Y")
            if end_date < start_time:
                print("Error: Начальная дата позже конечной даты.")
                return
        except ValueError:
            print("Error: Неверный формат даты.")
            return

        print("Все заметки:")
        for id, data in zametki.items():
            zametka_data = time.strptime(data.get('currentDate'), "%a %b %d %H:%M:%S %Y")
            if start_time <= zametka_data <= end_date:
                print(f"№ {data.get('id', 'N/A')};"
                      f" {data.get('titleZametka', 'N/A')};"
                      f" Дата: {data.get('currentDate', 'N/A')}")

        zametka_id = input("Открыть свою заметку? Введите ID. Хотите назад? Введите \"no\": ")
        if zametka_id.lower() != "no":
            show_zametka_body(zametki, zametka_id)
    else:
        print("Заметок нет.")

def show_zametka_body(zametki, zametka_id):
    try:
        if zametka_id in zametki:
            print(f"Заметка № {zametka_id}: {zametki[zametka_id]['titleZametka']}")
            print(zametki[zametka_id]['bodyZametka'])
            print()
        else:
            print("Заметка с таким ID не найдена.\n")
    except ValueError:
        print("Неверный ввод.\n")


def add(zametki, id_counter):
    titleZametka = input("Введите название заметки: ")
    bodyZametka = input("Введите свою заметку:\n")
    currentDate = time.ctime(time.time())

    entry_id = str(id_counter)
    for key, value in zametki.items():
        if 'id' in value and value['id'] == id_counter:
            entry_id = str(id_counter + 1)

    zametki[entry_id] = {'id': entry_id, 'titleZametka': titleZametka, 'bodyZametka': bodyZametka, 'currentDate': currentDate}
    save(zametki)

def delete(zametki):
    if (zametki):
        zametka_id = input("Введите ID заметки для ее удаления: ")
        try:
            if zametka_id in zametki:
                del zametki[zametka_id]
                print("Заметка удалена.\n")
                save(zametki)
            else:
                print("Заметка с таким ID не была найдена.\n")
        except ValueError:
            print("Неверный ввод. Введите ID заметки.")
    else:
        print("Заметок нет.")


def change(zametki):
    if (zametki):
        zametka_id = input("Введите ID заметки для ее изменения: ")
        try:
            if zametka_id in zametki:
                new_title = input("Введите новое название своей заметки: ")
                new_body = input("Введите свою новую заметку:\n")
                zametki[zametka_id]['titleZametka'] = new_title
                zametki[zametka_id]['bodyZametka'] = new_body
                zametki[zametka_id]['currentDate'] = time.ctime(time.time())
                print("Заметка успешно изменена.\n")
                save(zametki)
            else:
                print("Заметка с таким ID не найдена.\n")
        except ValueError:
            print("Неверный ввод. Введите ID заметки.")
    else:
        print("Заметок нет.")

zametki = load()
id_counter = len(zametki) + 1

info = ('Доступные команды: \n'
        'load - загружает заметки из файла\n'
        'all - показывает все заметки\n'
        'date - показывает заметки созданные, в указанных датах\n'
        'info - показывает информацию по командам программы\n'
        'delete - удаляет заметку с выбранным ID\n'
        'change - изменяет заметку\n'
        'exit - выход из программы')

while True:
    command = input("Введите одну из команд: info, load, all, date, add, delete, change, exit\n")

    if command == "exit":
        print("До свидания!")
        break

    elif command == "info":
        print(info)

    elif command == "load":
        notes = load()

    elif command == "all":
        showAll(zametki)

    elif command == "date":
        showDate(zametki)

    elif command == "add":
        add(zametki, id_counter)
        id_counter += 1

    elif command == "delete":
        delete(zametki)

    elif command == "change":
        change(zametki)

    else:
        print('Вы ввели неверную команду! Для списка команд обратитесь к "info"!')