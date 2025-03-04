import random

from aiogram import F, types, Router, Bot
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from database.orm_query import *
from filter.chat_types import ChatTypeFilter
from handlers.quiz_function import get_topics
from keyboard.inline import *
from sqlalchemy.future import select
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

start_functions_private_router = Router()
start_functions_private_router.message.filter(ChatTypeFilter(['private']))

welcome_text = (
    "👋 Привет !\n\n"
    "🎓 Добро пожаловать в EduQuiz — вашего персонального помощника в обучении!\n\n"
    "📚 Знания — это сила, а обучение может быть увлекательным! С EduQuiz вы сможете\n"
    "🔹 Проверять свои знания\n"
    "🔹 Закреплять новый материал\n"
    "🔹 Учиться в удобное время и в игровом формате\n\n"
    "🚀 Готовы прокачать свой интеллект? Давайте начнем!"
)
photo=types.FSInputFile('media/img.png')

@start_functions_private_router.message(CommandStart())
async def start_cmd(message: types.Message,session: AsyncSession):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    users = await orm_get_id_bot_user(session)
    if user_id not in users:
        name = f"{message.from_user.first_name}"
        username = f"@{message.from_user.username}" if message.from_user.username else ''
        await orm_add_bot_users(session, user_id=user_id, name=name, username=username)

    await message.answer_photo(
        photo=types.FSInputFile('media/img.png'),
        caption=welcome_text,
        reply_markup= start_functions_keyboard()
    )


@start_functions_private_router.callback_query(F.data == "start")
async def start_main_menu(query: types.CallbackQuery, ):
    """Обработчик callback_query для основного меню"""
    await query.message.edit_caption(
        caption=welcome_text,
        reply_markup=start_functions_keyboard())


@start_functions_private_router.callback_query(F.data == "start_")
async def start_main_menu(query: types.CallbackQuery, ):
    """Обработчик callback_query для основного меню"""
    await query.message.delete()
    await query.message.answer_photo(
        photo=types.FSInputFile('media/img.png'),
        caption=welcome_text,
        reply_markup=start_functions_keyboard()
    )


@start_functions_private_router.callback_query(F.data == "about_eduquiz")
async def about_eduquiz (query: types.CallbackQuery, ):
    about_eduquiz_text = (
        "🏢 *О проекте EduQuiz*\n\n"
        "EduQuiz — это образовательная платформа, которая предоставляет различные тесты и обучающие материалы для улучшения знаний. 🌐📚\n\n"

        "🤖 **В EduQuiz Боте**\n"
        "В нашем Telegram-боте вы можете:\n"
        "✅ Пройти различные викторины\n"
        "✅ Получить свою статистику и результаты\n"
        "✅ Просмотреть полезные видео для обучения\n"
        "✅ Связаться с поддержкой для получения помощи\n\n"

        "🌐 **На Сайте EduQuiz**\n"
        "На нашем сайте доступны более расширенные функции, включая:\n"
        "🖥️ *Тайпинг тесты*: проверка скорости и точности печати.\n"
        "💻 *Тесты по программированию*: тесты по различным языкам программирования и алгоритмам.\n"
        "👩‍🏫 *Викторины для учителей*: инструменты для создания викторин и тестов для студентов.\n"
        "🎥 *Полезные видео*: обучающие видеоматериалы по различным темам.\n\n"
        "Зайдите на наш сайт для более подробной информации и полного функционала!"
    )
    await query.message.edit_caption(
        caption=about_eduquiz_text,
        reply_markup=return_menu_functions_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )


@start_functions_private_router.callback_query(F.data == "contact_us")
async def contact_us (query: types.CallbackQuery, ):
    contact_info = (
        "📞 *Контакты для поддержки*\n\n"
        "Если у вас возникли вопросы или проблемы, вы можете связаться с нами:\n"
        "✉️ Email: duishobaevislam01@gmail.com\n"
        "📱 Telegram: @duishobaevislam01"
    )
    await query.message.edit_caption(
        caption=contact_info,
        reply_markup=return_menu_functions_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )


@start_functions_private_router.callback_query(F.data == 'faq')
async def faq_callback_query(query: types.CallbackQuery) -> None:
    caption_text = (
        "Часто задаваемые вопросы:\n\n"
        "Выберите интересующий вас вопрос из списка ниже:"
    )
    await query.message.edit_caption(
        caption=caption_text,
        reply_markup=generate_faq_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )


@start_functions_private_router.callback_query(F.data.startswith('faq_'))
async def faq_answer_callback(query: types.CallbackQuery) -> None:
    index = int(query.data.split('_')[1])
    question = FAQ[index]["question"]
    answer = FAQ[index]["answer"]

    caption_text = f"<b>{question}</b>\n\n{answer}"
    await query.message.edit_caption(
        caption=caption_text,
        reply_markup=return_menu_functions_keyboard(),
        parse_mode=ParseMode.HTML
    )


async def get_videos():
    url = "https://eduquiz-back-end.onrender.com/api/v1/videos/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return []


@start_functions_private_router.callback_query(F.data == 'useful_videos')
async def useful_videos_callback_query(query: types.CallbackQuery) -> None:
    videos = await get_videos()
    if videos:
        keyboard = generate_video_keyboard(videos)
        await query.message.edit_caption(
            caption="🎥 Вот список полезных видео для обучения:",
            reply_markup=keyboard,
        )
    else:
        await query.message.edit_caption(
            caption="К сожалению, 🎥 полезные видео не доступны в данный момент."
        )


@start_functions_private_router.callback_query(F.data == 'my_stats')
async def my_stats_callback(query: types.CallbackQuery, session: Session) -> None:
    user_id = query.from_user.id

    async with session.begin():
        result = await session.execute(
            select(
                QuizResult.score,
                QuizResult.total_questions,
                QuizResult.created_at,
                func.sum(QuizResult.score).filter(QuizResult.user_id == user_id).label("total_score"),
                func.count(QuizResult.id).filter(QuizResult.user_id == user_id).label("total_tests"),
                func.max(QuizResult.score).filter(QuizResult.user_id == user_id).label("best_score"),
                func.max(QuizResult.total_questions).filter(QuizResult.user_id == user_id).label("best_total_questions")
            ).where(QuizResult.user_id == user_id)
            .order_by(QuizResult.created_at.desc())
            .limit(1)
        )
        row = result.first()

    if row and all(row):
        score, total_questions, created_at, total_score, total_tests, best_score, best_total_questions = row

        caption_text = (
            "📊 <b>Ваша статистика:</b>\n\n"
            f"✅ Правильных ответов в последнем тесте: {score}/{total_questions}\n"
            f"🔢 Ваш общий балл за все тесты: {total_score or 0} 🔥\n"
            f"📈 Средний результат: {round(total_score / total_tests, 2) if total_tests else 0}\n"
            f"🏆 Лучший результат: {best_score}/{best_total_questions}\n"
            f"📝 Количество пройденных тестов: {total_tests}\n"
            f"⏰ Последний тест был пройден: {created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        )

        await query.message.edit_caption(
            caption=caption_text,
            reply_markup=return_menu_functions_keyboard(),
            parse_mode=ParseMode.HTML
        )
    else:
        await query.message.edit_caption(
            caption="🚫 У вас нет результатов тестов.",
            reply_markup=return_menu_functions_keyboard(),
        )


class QuizState(StatesGroup):
    current_question = State()
    correct_answers = State()

@start_functions_private_router.callback_query(F.data.startswith("start_quiz"))
async def start_quiz_callback(query: types.CallbackQuery) -> None:
    topics = await get_topics()
    keyboard = InlineKeyboardBuilder()
    for topic in topics:
        keyboard.add(InlineKeyboardButton(text=topic["name"], callback_data=f"select_topic_{topic['id']}"))
    keyboard.button(text="⬅️ Назад", callback_data="start")
    await query.message.edit_caption(caption="Выберите тему:", reply_markup=keyboard.adjust(1).as_markup())


@start_functions_private_router.callback_query(F.data.startswith("select_topic_"))
async def select_topic(update: types.CallbackQuery, state: FSMContext) -> None:
    topic_id = int(update.data.split("_")[2])
    topics = await get_topics()
    topic = next(topic for topic in topics if topic['id'] == topic_id)
    random_questions = random.sample(topic["questions"], 5)
    await state.set_data({"questions": random_questions, "current_question": 0, "correct_answers": 0})

    question = random_questions[0]
    options = [
        question["option_a"],
        question["option_b"],
        question["option_c"],
        question["option_d"]
    ]

    keyboard = InlineKeyboardBuilder()
    for option in options:
        keyboard.add(InlineKeyboardButton(text=option, callback_data=f"answer_{question['id']}_{option}"))
    keyboard.button(text="⬅️ Назад", callback_data="start")

    if "image" in question and question["image"]:
        await update.message.delete()
        await update.message.answer_photo(
            photo=question["image"],
            caption=question["text"],
            reply_markup=keyboard.adjust(1).as_markup()
        )
    else:
        await update.message.delete()
        await update.message.answer_photo(
            photo=photo,
            caption=question["text"],
            reply_markup=keyboard.adjust(1).as_markup()
        )


@start_functions_private_router.callback_query(F.data.startswith("answer_"))
async def answer_question(update: types.CallbackQuery, state: FSMContext, session: Session) -> None:
    data = update.data.split("_")
    question_id = int(data[1])
    selected_option = data[2]

    state_data = await state.get_data()
    questions = state_data["questions"]
    current_question_idx = state_data["current_question"]

    correct_answers = state_data.get("correct_answers", 0)

    question = next(q for q in questions if q["id"] == question_id)
    correct_answer = question["correct_answer"]

    if selected_option.upper() == correct_answer:
        correct = True
        correct_answers += 1
    else:
        correct = False

    await state.update_data(correct_answers=correct_answers)

    if correct:
        await update.answer("Правильный ответ!")
    else:
        await update.answer(f"Неправильный ответ! Правильный: {correct_answer}")

    next_question_idx = current_question_idx + 1
    if next_question_idx < len(questions):
        question = questions[next_question_idx]
        options = [
            ("A", question["option_a"]),
            ("B", question["option_b"]),
            ("C", question["option_c"]),
            ("D", question["option_d"])
        ]
        keyboard = InlineKeyboardBuilder()
        for option, text in options:
            keyboard.add(InlineKeyboardButton(text=text, callback_data=f"answer_{question['id']}_{option}"))
        keyboard.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="start"))

        if "image" in question and question["image"]:
            await update.message.delete()
            await update.message.answer_photo(
                photo=question["image"],
                caption=question["text"],
                reply_markup=keyboard.adjust(1).as_markup()
            )
        else:
            await update.message.delete()
            await update.message.answer_photo(
                photo=photo,
                caption=question["text"],
                reply_markup=keyboard.adjust(1).as_markup()
            )
        await state.update_data(current_question=next_question_idx)
    else:
        # Сохраняем результаты викторины в базе данных
        correct_answers = state_data["correct_answers"]
        total_questions = len(questions)

        # Сохраняем результат
        result = await save_quiz_result(update.from_user.id, correct_answers, total_questions, session)

        # Отправляем сообщение с результатом
        await update.message.edit_caption(
            caption=(
                f"<b>🎉 Викторина завершена!</b>\n"
                f"<i>Ваш результат:</i> <b>{correct_answers}/{total_questions}</b> 🏆\n\n"
                f"<b>✅ Правильные ответы:</b> {correct_answers} 🟢\n"
                f"<b>❌ Неправильные ответы:</b> {total_questions - correct_answers} 🔴\n\n"
                f"<i>Спасибо за участие! Надеемся, вам понравилось! 🙌</i>\n"
                f"<i>Присоединяйтесь к нам снова! 💪</i>"
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=return_menu_functions_keyboard()
        )

        # Очищаем состояние
        await state.clear()



