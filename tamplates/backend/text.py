import csv
import socket
import time

# Відкриваємо файл для читання
with open("devices.csv", "r") as csvfile:

    # Створюємо об'єкт reader для читання даних з файлу
    reader = csv.reader(csvfile, delimiter=";")

    # Проходимо по рядках файлу
    for row in reader:

        # Витягуємо IP-адресу пристрою
        ip_address = row[3]

        # Створюємо сокет
        socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Спробуємо з'єднатися з пристроєм
        try:
            socket.connect((ip_address, 80))
            socket.close()
            print(f"IP-адреса {ip_address} доступна")
        except socket.timeout:
            print(f"IP-адреса {ip_address} недоступна")


def check_availability():
    print("Все працює")

def main():
    while True:
        check_availability()
        time.sleep(3)

if __name__ == "__main__":
    main()