import csv
import json
import xml.etree.ElementTree as ET
from urllib.parse import urljoin
import requests


def remove_newline_from_end(devices='static\devices.csv'):
    with open(devices, 'r', encoding='utf-8') as file:
        file_content = file.read().replace('\n', r'\n')
        if file_content.endswith('\\n'):
            file_content = file_content[:-2]
        else:
            print('false')

    file_content = file_content.replace('\\n', '\n')
    with open(devices, 'w', encoding='utf-8') as file:
        file.write(file_content)

def check_and_write_text(text, csv_file_path='static\devices.csv'):
    # Відкриття CSV-файлу
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
        # Читання існуючого вмісту CSV-файлу
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as readfile:
            existing_content = readfile.read()

        # Перевірка, чи вже є такий текст
        if text in existing_content:
            print(f"Текст '{text}' вже існує у CSV-файлі.")
            return

        # Заміна \n на пробіл перед текстом, якщо він не на початку файла
        if existing_content:
            existing_content = existing_content.rstrip('\n') + '\n' + text
        else:
            existing_content = text

        # Запис нового вмісту у CSV-файл
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as writefile:
            writefile.write(existing_content)

        return (f"Текст '{text}' успішно додано до CSV-файлу.")

def delete_row_by_string(row_to_remove, csv_file_path='static\devices.csv'):
    # Відкриття CSV-файлу для читання
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Пошук і видалення рядку з вказаною IP-адресою
    new_lines = [line for line in lines if row_to_remove not in line]

    # Запис оновленого вмісту назад у файл
    with open(csv_file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)


# ======================================CONDER====================================================================
def copy_json_to_result_csv(ip_conder, conder_csv, new_csv_file):
    url = urljoin(ip_conder, '/ODJET_CGI?pread=all')
    data_list_csv = []
    response = requests.get(url)
    if response.status_code == 200:
        # Додавання завантажених даних до data_json
        data_json = response.text

        # Перетворюємо JSON у об'єкт Python
        data = json.loads(data_json)

        # Створюємо масив у вказаному форматі
        data_list_json = [[item["addr"], item["value"]] for item in data["tab_param"]]

        # Виводимо результат
        # print(result_array)

        with open(conder_csv, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file, delimiter=';')
            for row in csv_reader:
                data_list_csv.append(row)

        for item_data_list_json in data_list_json:
            for item_data_list_csv in data_list_csv:
                if item_data_list_json[0] == item_data_list_csv[0]:
                    new_item_data_list_json = int(item_data_list_json[1]) / int(item_data_list_csv[3])
                    item_data_list_csv.append(str(new_item_data_list_json))

        with open(new_csv_file, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';')
            csv_writer.writerows(data_list_csv)
    else:
        print("Не вдалося отримати дані з веб-сторінки. Код статусу:", response.status_code)


def conder(ip_conder='http://172.18.96.90'):
    conder_csv = 'static/devices/conder.csv'
    new_csv_file = 'static/conder.csv'
    devices = 'static/devices.csv'
    copy_json_to_result_csv(ip_conder, conder_csv,new_csv_file)
    copy_id = [2009, 2102, 2105, 3007, 3008, 3029, 3030]
    add_text = []
    with open(new_csv_file, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')

        for row in csv_reader:
            if int(row[0]) in copy_id:
                add_text.append(f'{row[2]}: {row[4]}')

    # ========================================

    with open(devices, 'r', newline='', encoding='utf-8') as devices_file:
        reader = csv.reader(devices_file, delimiter=';')
        rows = list(reader)
    for i in range(len(rows)):
        if ip_conder in rows[i][2]:
            if len(rows[i]) >= 4:  # Перевірка, чи існує четвертий стовпець
                rows[i][3] = ', '.join(add_text)
            else:
                rows[i].append(', '.join(add_text))  # Додавання четвертого стовпця та даних з ups_array

    with open(devices, 'w', newline='', encoding='utf-8') as devices_file:
        writer = csv.writer(devices_file, delimiter=';')
        writer.writerows(rows)

# ======================================UPS====================================================================
def ups(ups_path_csv='static/devices/ups.csv', ip_ups='https://172.18.97.21'):
    path_ups_ident_xml = urljoin(ip_ups,'/webpages/xml/ups/info_ident.xml')
    path_ups_battery_xml = urljoin(ip_ups,'/webpages/xml/ups/info_battery.xml')
    path_ups_io_xml = urljoin(ip_ups,'/webpages/xml/ups/info_io.xml')
    column_csv_input_values = []

    with open(ups_path_csv, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if row:  # Перевірка, чи рядок не пустий
                column_csv_input_values.append(row[0])

    result_array_ident = result_parce_xml(path_ups_ident_xml)
    result_array_battery = result_parce_xml(path_ups_battery_xml)
    result_array_io = result_parce_xml(path_ups_io_xml)

    new_array_ident = compare_arrays(column_csv_input_values, result_array_ident)
    new_array_battery = compare_arrays(column_csv_input_values, result_array_battery)
    new_array_io = compare_arrays(column_csv_input_values, result_array_io)

    result_array_csv = merge_arrays(new_array_ident,merge_arrays(new_array_battery,new_array_io))

    update_csv_file(ups_path_csv, result_array_csv, f"static/ups_{ip_ups[-2:]}.csv")

    add_info_to_devices(f"static/ups_{ip_ups[-2:]}.csv", 'static/devices.csv', ip_ups)

def compare_arrays(column_array, result_array):
    new_array_csv = []

    for column_value in column_array:
        found = False

        for result_pair in result_array:
            if result_pair[0] == column_value:
                new_array_csv.append(result_pair)
                found = True
                break

        if not found:
            new_array_csv.append([column_value])

    return new_array_csv

def result_parce_xml(path_ups_ident_xml):
    try:
        # Fetch XML data from the URL, bypassing SSL certificate verification
        response = requests.get(path_ups_ident_xml, verify=False)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Store XML data in a variable
            xml_data = response.text

            # Print the XML data


        else:
            print(f"Error: Unable to fetch XML data. Status code: {response.status_code}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Розбираємо XML
    root = ET.fromstring(xml_data)

    # Створюємо масив для зберігання пар ідентифікаторів та їх значень
    result_array = []

    # Ітеруємося по всіх елементах XML
    for element in root.iter():
        # Ігноруємо елементи без атрибутів
        if element.attrib:
            # Додаємо пару ідентифікатора та значення до масиву
            result_array.append([element.attrib['id'], element.text])

    result_array = remove_tabs_from_array(result_array)
    return result_array

def remove_tabs_from_array(input_array):
    cleaned_array = []
    for sub_array in input_array:
        cleaned_sub_array = [value.replace('\t\t', '') if isinstance(value, str) else value for value in sub_array]
        cleaned_array.append(cleaned_sub_array)
    return cleaned_array

def merge_arrays(array1, array2):
    merged_array = []

    for item1 in array1:
        for item2 in array2:
            if item1[0] == item2[0]:
                if len(item1) == 2:
                    merged_array.append(item1)
                else:
                    merged_array.append(item2)

    return merged_array

def update_csv_file(input_csv_file, input_array, output_csv_file):
    with open(input_csv_file, 'r', newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        rows = list(reader)

    for array_item in input_array:
        for row in rows:
            if array_item[0] == row[0]:
                if len(row) >= 5:
                    if row[3] != '0':
                        row[4] = f"{array_item[1]} {row[3]}"
                    else:
                        row[4] = array_item[1]

    with open(output_csv_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerows(rows)

def add_info_to_devices(ups, devices_csv, ip_ups):
    # Зчитуємо дані з файлів
    ups_array=[]
    with open(ups, 'r', newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        for row in reader:
            ups_array.append(f'{row[2]}: {row[-1]}')

    # Виведемо зміст масиву ups_array

    with open(devices_csv, 'r', newline='', encoding='utf-8') as devices_file:
        reader = csv.reader(devices_file, delimiter=';')
        rows = list(reader)
    for i in range(len(rows)):
        if ip_ups in rows[i][2]:
            if len(rows[i]) >= 4:  # Перевірка, чи існує четвертий стовпець
                rows[i][3] = ', '.join(ups_array)
            else:
                rows[i].append(', '.join(ups_array))  # Додавання четвертого стовпця та даних з ups_array

    with open(devices_csv, 'w', newline='', encoding='utf-8') as devices_file:
        writer = csv.writer(devices_file, delimiter=';')
        writer.writerows(rows)


# ======================================ADD_TO_FILE====================================================================
def add_text_to_devices(devices_file_path='static/devices.csv'):
    data_array = []

    with open(devices_file_path, 'r', newline='', encoding='utf-8') as devices_file:
        reader = csv.reader(devices_file, delimiter=';')
        for row in reader:
            if len(row) >= 3:  # Перевірка, чи є достатньо стовпців
                data_array.append([row[0], row[2]])
                if row[0] == 'Кондиціонер':
                    conder(row[2])
                elif row[0] == 'ДБЖ':
                    ups(ip_ups=row[2])










