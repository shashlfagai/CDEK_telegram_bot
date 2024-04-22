# Установка необходимых зависимостей с помощью pip
#!pip install telebot
#!pip install pillow
#!pip install python-barcode
#!pip install pyzbar

# Импорт необходимых модулей
import telebot  # Импорт модуля для работы с Telegram API
import os  # Импорт модуля для работы с операционной системой
from pyzbar.pyzbar import decode  # Импорт функции для декодирования штрих-кодов
from PIL import Image  # Импорт модуля для работы с изображениями
from barcode.writer import ImageWriter  # Импорт класса для создания изображений штрих-кодов
from barcode import Code128  # Импорт класса для создания штрих-кодов формата Code128

# Установка токена для доступа к боту Telegram
bot_token = "7101871510:AAHnSRSUQXym5qT3OYnPO4wdRXIvlrGThVc"
bot = telebot.TeleBot(bot_token)  # Создание экземпляра бота с использованием полученного токена


# Обработчик сообщений, реагирующий на получение фото
@bot.message_handler(content_types=['photo'])
def handle_image(message):
    try:
        # Получение информации о загруженном фото
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("image.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
        img = Image.open('image.jpg')  # Открытие изображения

        # Декодирование штрих-кода на изображении
        detected_barcodes = decode(img)
        if len(detected_barcodes) > 1:
            bdata = detected_barcodes[1].data.decode('utf-8')
            my_code = Code128(bdata, writer=ImageWriter())
            my_code.save("barcode")
            with open("barcode.png", 'rb') as barcode_file:
                bot.send_photo(message.chat.id, barcode_file)  # Отправка изображения с штрих-кодом
            os.remove("barcode.png")
        else:
            # Декодирование изображения с штрих-кодом
            if detected_barcodes:
                bdata = detected_barcodes[0].data.decode('utf-8')
                my_code = Code128(bdata, writer=ImageWriter())
                my_code.save("barcode")
                with open("barcode.png", 'rb') as barcode_file:
                    bot.send_photo(message.chat.id, barcode_file)  # Отправка изображения с штрих-кодом
                os.remove("barcode.png")
            else:
                bot.reply_to(message, "Штрих-код не найден на изображении.")
        
        os.remove("image.jpg")  # Удаление загруженного изображения
        if os.path.exists("cropped_image.jpg"):  # Проверка существования файла перед его удалением
            os.remove("cropped_image.jpg")  # Удаление обрезанного изображения
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")  # Отправка сообщения об ошибке в случае исключения

bot.polling()  # Запуск бота и ожидание получения сообщений
