import csv, os, sys, subprocess
from collections import OrderedDict
from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton
from aiogram.dispatcher.filters import Text
from func import check_and_write_text, delete_row_by_string, remove_newline_from_end, add_text_to_devices

# Замініть 'your_bot_token' на ваш токен бота
bot_token = '5884178179:AAH3vk1wVcTd7abUtrNdcglDl_1_0q70N4w'
bot = Bot(token=bot_token)
dp = Dispatcher(bot)

# File with bot code
bot_file = "bot.py"


# Додаємо middleware для гарячого перезавантаження

def read_csv(file_path='static/devices.csv', delimiter=';'):
    data = []

    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=delimiter)
        for row in csv_reader:
            data.append(row)

    return data

array_read_csv = read_csv()

# print(array_read_csv)

# Функція для створення клавіатури з кнопками
def create_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for row in array_read_csv:
        if len(row) >= 3:  # Перевірка, чи є достатньо елементів у рядку
            button_text = f"{row[1]}: {row[2]}"
            button = types.KeyboardButton(button_text)
            keyboard.add(button)

    return keyboard
def restart():
    current_directory = os.getcwd()
    # Формування шляху до файлу
    script_path = os.path.join(current_directory, "bot.py")
    # Виклик команди для перезапуску Python-скрипту
    subprocess.Popen([sys.executable, script_path])
    # Вихід з поточного процесу, таким чином, бот перезапуститься
    sys.exit()
# print(create_keyboard())

def create_del_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for row in array_read_csv:
        if len(row) >= 3:  # Перевірка, чи є достатньо елементів у рядку
            button_text = f"{row[1]} - {row[2]}"
            button = types.KeyboardButton(button_text)
            keyboard.add(button)

    return keyboard
def create_add_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    unique_names_buttons = list(OrderedDict.fromkeys(row[0] for row in array_read_csv))
    buttons = [KeyboardButton(name) for name in unique_names_buttons]
    keyboard.add(*buttons)
    return keyboard
# print(list(OrderedDict.fromkeys(row[0] for row in array_read_csv)))
# print(create_add_button())
array_create_add_button = create_add_keyboard()
# Змінна для визначення, чи очікується введення IP-адреси
# Обробник команди /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    # Отримати нопки із масиву
    keyboard = create_keyboard()
    new_buttons_row = [
        {"text": "Додати девайс"},
        {"text": "Видалити девайс"}
    ]
    keyboard["keyboard"].append(new_buttons_row)
    await message.reply("Оберіть пристрій:", reply_markup=keyboard)

# Обробник для натискання на кнопку
@dp.message_handler(lambda message: message.text in [f"{row[1]}: {row[2]}" for row in array_read_csv])
async def handle_button_click(message: types.Message):
    # Знаходимо рядок, який відповідає натиснутій кнопці
    clicked_row = [row for row in array_read_csv if f"{row[1]}: {row[2]}" == message.text]

    if clicked_row and len(clicked_row[0]) >= 4:
        info_message = clicked_row[0][3]

        # Замінити коми (,) на символ нового рядка (\n)
        info_message = info_message.replace(',', '\n')

        # Відправити повідомлення з розділеними на окремі рядки даними
        await message.answer(info_message)

@dp.message_handler(lambda message: message.text.startswith('Кондиціонер;h'))
async def handle_condenser_message(message: types.Message):
    input_text = message.text
    parts = input_text.split(';')

    if len(parts) >= 2:
        modified_array = [parts[0] + ';', parts[0] + ';' + parts[1] + ';']
        final_text = ''.join(modified_array)
        check_and_write_text(final_text)
        add_text_to_devices()
        remove_newline_from_end()
        await message.answer(f'Додано пристрій {parts[0]}: {parts[1]}')
        add_text_to_devices()
        remove_newline_from_end()
        restart()
    else:
        await message.answer("Неправильний формат рядка.")

@dp.message_handler(lambda message: message.text.startswith('ДБЖ;h'))
async def handle_condenser_message(message: types.Message):
    input_text = message.text
    parts = input_text.split(';')

    if len(parts) >= 2:
        modified_array = [parts[0] + ';', parts[0] + ';' + parts[1] + ';']
        final_text = ''.join(modified_array)
        check_and_write_text(final_text)
        add_text_to_devices()
        remove_newline_from_end()
        await message.answer(f'Додано пристрій {parts[0]}: {parts[1]}')
        add_text_to_devices()
        remove_newline_from_end()
        restart()
    else:
        await message.answer("Неправильний формат рядка.")

@dp.message_handler(Text(equals='Назад до головного меню'))
async def back_to_main_menu(message: types.Message):
    # Викликати обробник команди /start
    await start_command(message)

@dp.message_handler(lambda message: message.text.lower() == 'eror')
async def handle_error_message(message: types.Message):
    notification_text = ("Увага!!! Пристрій: Кондиціонер, на локації http://172.18.96.90. "
                         "Значення: Температура в кімнаті. Значення критично низьке")
    await bot.send_message(chat_id=message.chat.id, text=notification_text)


#Видалення пристрою
@dp.message_handler(Text(equals='Видалити девайс'))
async def add_remove(message: types.Message):
    keyboard = create_del_keyboard()
    new_buttons_row = [
        {"text": "Назад до головного меню"}
    ]
    keyboard["keyboard"].append(new_buttons_row)
    await message.answer("Видалити існуючий девайс", reply_markup=keyboard)
    add_text_to_devices()
    remove_newline_from_end()

@dp.message_handler(Text(equals='Додати девайс'))
async def add_device(message: types.Message):
    await message.answer("Інформація по додаванню девайсів\n"
                         "Через певні обмеження при розробці додавання девайсів із чат-боту проходять вручну\n"
                         "Вам, як користувачеві необхідно прописати назву девайсу то його ip-адресу\n"
                         "Формат: 'Назва пристрою';'ip-адреса пристрою';\n"
                         "Приклад: ДБЖ;https://172.18.97.22;\n"
                         "Також натисканням на дану кнопку ви перезавантажуєте телеграм-бот")

    add_text_to_devices()
    remove_newline_from_end()
    restart()


@dp.message_handler(lambda message: message.text in [f"{row[1]} - {row[2]}" for row in array_read_csv])
async def handle_button_click(message: types.Message):
    # Знаходимо рядок, який відповідає натиснутій кнопці
    clicked_row = [row for row in array_read_csv if f"{row[1]} - {row[2]}" == message.text]

    if clicked_row and len(clicked_row[0]) >= 4:
        delete_row_by_string(clicked_row[0][2])
        add_text_to_devices()
        remove_newline_from_end()
        info_message = f'Видалено пристрій {clicked_row[0][1]}: {clicked_row[0][2]}'
        await message.answer(info_message)
        add_text_to_devices()
        remove_newline_from_end()
        restart()



# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)