"""
Team applications handler with professional architecture.
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.application import ApplicationType
from app.services.application import ApplicationService
from app.services.notification import NotificationService
from app.utils.keyboards import get_back_button, get_team_cancel_button, get_main_menu
from app.core.logger import get_logger

logger = get_logger(__name__)
router = Router(name="team")


class TeamApplicationForm(StatesGroup):
    """States for team application form."""
    waiting_for_name = State()
    waiting_for_activity = State()
    waiting_for_experience = State()
    waiting_for_portfolio = State()


@router.callback_query(F.data == "join_team")
async def join_team_start(
    callback: CallbackQuery,
    state: FSMContext,
    user: User
):
    """Start team application process."""
    logger.info(f"User {user.telegram_id} started team application")
    
    team_text = (
        "👥 <b>Присоединиться к команде NOFACE.digital</b>\n\n"
        "🚀 <b>Мы ищем талантливых профессионалов!</b>\n\n"
        "💡 <b>Кого мы ищем:</b>\n"
        "• Frontend/Backend разработчиков\n"
        "• UI/UX дизайнеров\n"
        "• DevOps инженеров\n"
        "• Project менеджеров\n"
        "• QA специалистов\n"
        "• Маркетологов\n\n"
        "🤝 <b>Станьте частью инновационной команды, которая создает будущее!</b>\n\n"
        "📝 <b>Заполните анкету и мы обязательно рассмотрим вашу кандидатуру!</b>\n\n"
        "👤 <b>Как вас зовут?</b>\n"
        "<i>Укажите ваше полное имя</i>"
    )
    
    # Удаляем предыдущее сообщение и отправляем новое с фото
    await callback.message.delete()
    await callback.message.answer_photo(
        photo="https://i.ibb.co/8DfjBpqs/FB6-A8-CA0-C656-4397-AEE1-4989-CC4-FE5-A2.png",
        caption=team_text,
        reply_markup=get_team_cancel_button(),
        parse_mode="HTML"
    )
    await state.set_state(TeamApplicationForm.waiting_for_name)
    await callback.answer("🎯 Начинаем заполнение анкеты!")


@router.message(TeamApplicationForm.waiting_for_name)
async def process_team_name(
    message: Message,
    state: FSMContext,
    user: User
):
    """Process applicant name."""
    name = message.text.strip()
    
    if len(name) < 2:
        await message.answer(
            "❌ <b>Имя слишком короткое</b>\n\n"
            "Пожалуйста, укажите корректное имя (минимум 2 символа)",
            parse_mode="HTML"
        )
        return
    
    await state.update_data(name=name)
    logger.info(f"User {user.telegram_id} provided name for team: {name}")
    
    activity_text = (
        f"👋 <b>Привет, {name}!</b>\n\n"
        "💼 <b>Чем вы занимаетесь профессионально?</b>\n\n"
        "🎯 <b>Примеры специализаций:</b>\n"
        "• Frontend Developer (React, Vue, Angular)\n"
        "• Backend Developer (Node.js, Python, Go)\n"
        "• Fullstack Developer\n"
        "• UI/UX Designer\n"
        "• Mobile Developer (iOS, Android, Flutter)\n"
        "• DevOps Engineer\n"
        "• Project Manager\n"
        "• QA Engineer\n"
        "• Data Scientist\n"
        "• Marketing Specialist\n\n"
        "<i>Опишите вашу основную специализацию и технологии</i>"
    )
    
    await message.answer(
        activity_text,
        reply_markup=get_team_cancel_button(),
        parse_mode="HTML"
    )
    await state.set_state(TeamApplicationForm.waiting_for_activity)


@router.message(TeamApplicationForm.waiting_for_activity)
async def process_team_activity(
    message: Message,
    state: FSMContext,
    user: User
):
    """Process professional activity."""
    activity = message.text.strip()
    
    if len(activity) < 5:
        await message.answer(
            "❌ <b>Описание деятельности слишком короткое</b>\n\n"
            "Пожалуйста, опишите вашу специализацию более подробно",
            parse_mode="HTML"
        )
        return
    
    await state.update_data(activity=activity)
    logger.info(f"User {user.telegram_id} provided activity: {activity}")
    
    experience_text = (
        "🎯 <b>Расскажите о вашем опыте</b>\n\n"
        "💡 <b>Опишите подробно:</b>\n"
        "• 📅 Сколько лет работаете в IT?\n"
        "• 🛠 С какими технологиями работали?\n"
        "• 🚀 Какие проекты реализовывали?\n"
        "• 🏆 Ключевые достижения?\n"
        "• 📚 Образование и сертификаты?\n"
        "• 💪 Сильные стороны?\n\n"
        "<i>Чем подробнее опишете опыт, тем лучше мы поймем ваш уровень</i>"
    )
    
    await message.answer(
        experience_text,
        reply_markup=get_team_cancel_button(),
        parse_mode="HTML"
    )
    await state.set_state(TeamApplicationForm.waiting_for_experience)


@router.message(TeamApplicationForm.waiting_for_experience)
async def process_team_experience(
    message: Message,
    state: FSMContext,
    user: User
):
    """Process work experience."""
    experience = message.text.strip()
    
    if len(experience) < 10:
        await message.answer(
            "❌ <b>Описание опыта слишком короткое</b>\n\n"
            "Пожалуйста, расскажите о своем опыте более подробно (минимум 10 символов)",
            parse_mode="HTML"
        )
        return
    
    await state.update_data(experience=experience)
    logger.info(f"User {user.telegram_id} provided experience: {len(experience)} characters")
    
    portfolio_text = (
        "🎨 <b>Последний шаг - портфолио</b>\n\n"
        "📂 <b>Поделитесь ссылками на ваши работы:</b>\n"
        "• 🌐 GitHub профиль\n"
        "• 🎨 Behance/Dribbble портфолио\n"
        "• 💼 LinkedIn профиль\n"
        "• 🖥 Личный сайт\n"
        "• 📱 Приложения в App Store/Google Play\n"
        "• 🔗 Другие ссылки на работы\n\n"
        "💡 <b>Альтернативы:</b>\n"
        "• Опишите проекты текстом, если нет ссылок\n"
        "• Укажите компании где работали\n"
        "• Напишите \"в процессе создания\" если только начинаете\n\n"
        "<i>Портфолио поможет нам лучше оценить ваши навыки</i>"
    )
    
    await message.answer(
        portfolio_text,
        reply_markup=get_team_cancel_button(),
        parse_mode="HTML"
    )
    await state.set_state(TeamApplicationForm.waiting_for_portfolio)


@router.message(TeamApplicationForm.waiting_for_portfolio)
async def process_team_portfolio(
    message: Message,
    state: FSMContext,
    user: User,
    db: Session
):
    """Process portfolio and create team application."""
    portfolio = message.text.strip()
    
    if len(portfolio) < 3:
        await message.answer(
            "❌ <b>Информация о портфолио слишком короткая</b>\n\n"
            "Пожалуйста, укажите ссылки на работы или опишите проекты",
            parse_mode="HTML"
        )
        return
    
    # Get form data
    data = await state.get_data()
    
    try:
        # Create team application
        app_service = ApplicationService(db)
        application = app_service.create_team_application(
            user=user,
            name=data['name'],
            activity=data['activity'],
            experience=data['experience'],
            portfolio=portfolio
        )
        
        # Send notification to admin
        notification_service = NotificationService(message.bot)
        notification_sent = await notification_service.send_application_notification(application)
        
        logger.info(
            f"Created team application #{application.id} for user {user.telegram_id}, "
            f"notification sent: {notification_sent}"
        )
        
        # Success message
        success_text = (
            "🎉 <b>Анкета успешно отправлена!</b>\n\n"
            f"📋 <b>Номер заявки:</b> #{application.id}\n"
            f"👤 <b>Имя:</b> {data['name']}\n"
            f"💼 <b>Специализация:</b> {data['activity']}\n\n"
            "⏰ <b>Что происходит дальше?</b>\n"
            "• 📧 Мы внимательно изучим вашу анкету\n"
            "• 🔍 Проведем первичный отбор (1-3 дня)\n"
            "• 📞 Свяжемся для технического интервью\n"
            "• 🤝 Обсудим условия сотрудничества\n\n"
            "🚀 <b>Спасибо за интерес к NOFACE.digital!</b>\n"
            "Мы всегда рады талантливым людям в нашей команде.\n\n"
            "💬 <b>Остались вопросы?</b> Пишите нам напрямую!"
        )
        
        await message.answer(
            success_text,
            reply_markup=get_back_button(),
            parse_mode="HTML"
        )
        
        # Clear state
        await state.clear()
        
    except Exception as e:
        logger.error(f"Error creating team application: {e}", exc_info=True)
        
        await message.answer(
            "❌ <b>Произошла ошибка при отправке анкеты</b>\n\n"
            "Пожалуйста, попробуйте позже или свяжитесь с нами напрямую",
            reply_markup=get_back_button(),
            parse_mode="HTML"
        )
        await state.clear()


@router.callback_query(F.data == "cancel_team")
async def cancel_team_application(
    callback: CallbackQuery,
    state: FSMContext,
    user: User
):
    """Cancel team application form."""
    current_state = await state.get_state()
    if not current_state or not current_state.startswith("TeamApplicationForm"):
        return
    
    await state.clear()
    logger.info(f"User {user.telegram_id} cancelled team application")
    
    cancel_text = (
        "❌ <b>Анкета отменена</b>\n\n"
        "😊 Не беда! Вы можете подать заявку в команду "
        "в любое удобное время.\n\n"
        "💡 <b>Готовы присоединиться к нам?</b>\n"
        "Мы всегда открыты для талантливых специалистов!"
    )
    
    # Проверяем, есть ли текст в сообщении для редактирования
    if callback.message.text:
        await callback.message.edit_text(
            cancel_text,
            reply_markup=get_back_button(),
            parse_mode="HTML"
        )
    else:
        # Если сообщение с фото - удаляем и отправляем новое
        await callback.message.delete()
        await callback.message.answer(
            cancel_text,
            reply_markup=get_back_button(),
            parse_mode="HTML"
        )
    await callback.answer("Анкета отменена") 