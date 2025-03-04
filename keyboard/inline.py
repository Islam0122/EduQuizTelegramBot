import aiohttp
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_functions_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🎮 Начать викторину", callback_data="start_quiz"))
    keyboard.add(InlineKeyboardButton(text="📊 Моя статистика", callback_data="my_stats"))
    keyboard.add(InlineKeyboardButton(text="🎥 Полезные видео", callback_data="useful_videos"))
    keyboard.add(InlineKeyboardButton(text="🏢 Про EduQuiz", callback_data="about_eduquiz"))
    keyboard.add(InlineKeyboardButton(text="🌐 Перейти на сайт", url="https://islam0122.github.io/EduQuiz_front-end/"))
    keyboard.add(InlineKeyboardButton(text="📅 Поддержка", callback_data="contact_us"))
    keyboard.add(InlineKeyboardButton(text="❓ Часто задаваемые вопросы", callback_data="faq"))
    return keyboard.adjust(2,1,1,1,1,1).as_markup()


def return_menu_functions_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🔙 Вернуться в главное меню", callback_data="start"))
    return keyboard.adjust(1, ).as_markup()


def return2_menu_functions_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🔙 Вернуться в главное меню", callback_data="start_"))
    return keyboard.adjust(1, ).as_markup()


def get_cancel_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="❌ Отменить", callback_data="cancel"))
    return keyboard.adjust(1).as_markup()


def start_admin_inline_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="📊 Статистика бота", callback_data="bot_statistics"),
        InlineKeyboardButton(text="➕ Добавить администратора", callback_data="add_admin"),
        InlineKeyboardButton(text="👥 Список администраторов", callback_data="list_admins")
    )
    return keyboard.adjust(2, 1).as_markup()


def return_admin_panel_functions_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🔙 Вернуться в главное меню", callback_data="start_admin"))
    return keyboard.adjust(1, ).as_markup()


FAQ = [
     {"question": "👨‍💻 Кто создал EduQuiz?",
      "answer": "EduQuiz был создан @duishobaevislam01 и @Adilet_dew, стремящихся сделать обучение интересным и доступным."},
    {"question": "🤖 Что такое EduQuiz?",
     "answer": "EduQuiz — это бот для проведения викторин и тестов, предназначенный для помощи в обучении."},
    {"question": "🎯 Зачем нужен EduQuiz?",
     "answer": "EduQuiz помогает пользователям улучшать свои знания через интерактивные тесты и викторины."},
    {"question": "🧑‍🏫 Для кого предназначен EduQuiz?",
     "answer": "EduQuiz предназначен для всех, кто хочет улучшить свои знания в разных областях."},
    {"question": "📚 Как начать использовать EduQuiz?",
     "answer": "Для начала просто нажмите на кнопку 'Пройти викторину' и выберите интересующую вас тему!"},
    {"question": "💡 Какие функции есть у EduQuiz?",
     "answer": "В EduQuiz доступны викторины, статистика прохождений, возможность обучения новым темам и многое другое!"},
    {"question": "🔧 Как связаться с поддержкой?",
     "answer": "Если у вас возникли вопросы или проблемы, вы всегда можете связаться с нами через раздел 'Поддержка'."}
]


def generate_faq_keyboard():
    builder = InlineKeyboardBuilder()
    for index, item in enumerate(FAQ):
        builder.button(text=item["question"], callback_data=f"faq_{index}")
    builder.button(text="⬅️ Назад", callback_data="start")
    return builder.adjust(1, ).as_markup()


def generate_video_keyboard(videos):
    keyboard =  InlineKeyboardBuilder()
    for video in videos:
        keyboard.add(InlineKeyboardButton(text=video["title"], url=video["video_url"]))
    keyboard.button(text="⬅️ Назад", callback_data="start")
    return keyboard.adjust(1,).as_markup()

