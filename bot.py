import io
import telebot
import os
from rembg import remove # u2net
from PIL import Image
import logging
from dotenv import load_dotenv

load_dotenv()

# Логирование бота
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BACKGROUND_IMAGE = os.getenv('BACKGROUND_IMAGE', 'background.jpg')

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Отправь изображение, чтобы я мог заменить его фон.')

def process_image(image_bytes):
    input_image = Image.open(io.BytesIO(image_bytes))
    output = remove(input_image)
    
    background = Image.open(BACKGROUND_IMAGE).convert('RGBA')
    background = background.resize(output.size)
    
    # Новое изобоажение с комбинированием фона и переднего плана
    composite = Image.new('RGBA', background.size)
    composite = Image.alpha_composite(composite, background)
    composite = Image.alpha_composite(composite, output)
    
    result_image = composite.convert('RGB')
    
    result_bytes = io.BytesIO()
    result_image.save(result_bytes, format='PNG')
    return result_bytes.getvalue()

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        bot.send_message(message.chat.id, 'Удаляю фон...')
        # Скачивание фото
        file_info = bot.get_file(message.photo[-1].file_id)

        # Загрузка изображения
        image_data = bot.download_file(file_info.file_path)
        
        processed_image = process_image(image_data)
        bot.send_photo(
            chat_id=message.chat.id,
            photo=processed_image,
            caption='Готово! Фон заменен.'
        )
        # bot.delete_message(message.chat.id, message.message_id)

    except Exception as e:
        logger.error(f'Ошибка обработки: {e}')
        bot.reply_to(message, f'Ошибка обработки изображения: {str(e)}')

if __name__ == '__main__':
    logger.info('Бот запущен')
    bot.infinity_polling()