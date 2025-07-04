"""
Start handler with modern architecture.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import Session

from app.models.user import User
from app.services.user import UserService
from app.core.config import settings
from app.utils.keyboards import get_main_menu, get_back_button
from app.core.logger import get_logger

logger = get_logger(__name__)
router = Router(name="start")


@router.message(CommandStart())
async def start_command(
    message: Message,
    db: Session,
    user: User,
    user_service: UserService
):
    """
    Handle /start command with modern DI approach.
    
    Args:
        message: Telegram message
        db: Database session (injected by middleware)
        user: User instance (injected by middleware)
        user_service: User service (injected by middleware)
    """
    logger.info(f"User {user.telegram_id} started the bot")
    
    welcome_text = (
        f"👋 <b>Добро пожаловать в {settings.bot_name}!</b>\n\n"
        "🚀 <b>NOFACE.digital</b> — команда профессиональных разработчиков\n\n"
        "💎 <b>Мы создаём:</b>\n"
        "• Высокопроизводительные веб-приложения\n"
        "• Интеллектуальные Telegram-боты\n" 
        "• Современные онлайн-магазины\n"
        "• Инновационные Web3 решения\n"
        "• Защищённые анонимные платформы\n"
        "• AI-интеграции нового поколения\n"
        "• Стартапы полного цикла\n\n"
        "🎯 <b>Выберите, что вас интересует:</b>"
    )
    
    await message.answer_photo(
        photo="https://i.ibb.co/3m4bCScL/AB6-FA99-A-E1-CA-4498-9-DE7-2-A64-DA7-B96-E4.png",
        caption=welcome_text,
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "back_to_main")
async def back_to_main(
    callback: CallbackQuery,
    user: User
):
    """Return to main menu."""
    logger.info(f"User {user.telegram_id} returned to main menu")
    
    welcome_text = (
        f"👋 <b>Добро пожаловать в {settings.bot_name}!</b>\n\n"
        "🚀 <b>NOFACE.digital</b> — команда профессиональных разработчиков\n\n"
        "💎 <b>Мы создаём:</b>\n"
        "• Высокопроизводительные веб-приложения\n"
        "• Интеллектуальные Telegram-боты\n" 
        "• Современные онлайн-магазины\n"
        "• Инновационные Web3 решения\n"
        "• Защищённые анонимные платформы\n"
        "• AI-интеграции нового поколения\n"
        "• Стартапы полного цикла\n\n"
        "🎯 <b>Выберите, что вас интересует:</b>"
    )
    
    # Всегда удаляем предыдущее сообщение и отправляем новое с фото
    await callback.message.delete()
    await callback.message.answer_photo(
        photo="https://i.ibb.co/3m4bCScL/AB6-FA99-A-E1-CA-4498-9-DE7-2-A64-DA7-B96-E4.png",
        caption=welcome_text,
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "direct_contact")
async def direct_contact(
    callback: CallbackQuery,
    user: User
):
    """Show direct contact information."""
    logger.info(f"User {user.telegram_id} requested direct contact")
    
    contact_text = (
        "📞 <b>Связаться напрямую</b>\n\n"
        "💬 <b>Telegram CEO:</b> @pavel_xdev\n"
        "🌐 <b>Сайт:</b> https://noface.digital\n\n"
        "⚡️ <b>Для срочных вопросов:</b>\n"
        "Пишите напрямую CEO @pavel_xdev для быстрой консультации\n\n"
        "🕐 <b>Время ответа:</b> в течение 2-4 часов\n"
        "🌍 <b>Работаем:</b> 24/7, любая временная зона"
    )
    
    # Удаляем сообщение с фото и отправляем новое с текстом
    await callback.message.delete()
    await callback.message.answer(
        contact_text,
        reply_markup=get_back_button(),
        parse_mode="HTML",
        disable_web_page_preview=True
    )
    await callback.answer(
        "💌 Контакты отправлены!",
        show_alert=False
    )


@router.callback_query(F.data == "company_info")
async def about_company(
    callback: CallbackQuery,
    user: User
):
    """Show company information."""
    logger.info(f"User {user.telegram_id} requested company info")
    
    about_text = (
        "ℹ️ <b>О компании NOFACE.digital</b>\n\n"
        "🚀 <b>Кто мы?</b>\n"
        "Команда профессиональных разработчиков с экспертизой "
        "в создании цифровых решений нового поколения.\n\n"
        
        "💎 <b>Наша миссия:</b>\n"
        "Превращать самые смелые идеи в работающие продукты, "
        "которые меняют бизнес и жизни людей.\n\n"
        
        "🎯 <b>Специализация:</b>\n"
        "• Высоконагруженные веб-приложения\n"
        "• Интеллектуальные Telegram-боты\n"
        "• E-commerce платформы\n"
        "• Блокчейн и Web3 решения\n"
        "• AI/ML интеграции\n"
        "• DevOps и инфраструктура\n\n"
        
        "🏆 <b>Наши принципы:</b>\n"
        "• Качество превыше всего\n"
        "• Современные технологии\n"
        "• Индивидуальный подход\n"
        "• Полная прозрачность\n"
        "• Соблюдение сроков\n\n"
        
        "⚡ <b>Почему выбирают нас:</b>\n"
        "• 5+ лет опыта в IT\n"
        "• 100+ успешных проектов\n"
        "• Команда Senior специалистов\n"
        "• Поддержка 24/7\n"
        "• Гарантия результата\n\n"
        
        "🌐 <b>Сайт:</b> https://noface.digital\n"
        "👨‍💼 <b>CEO:</b> @pavel_xdev"
    )
    
    # Удаляем сообщение с фото и отправляем новое с текстом
    await callback.message.delete()
    await callback.message.answer(
        about_text,
        reply_markup=get_back_button(),
        parse_mode="HTML",
        disable_web_page_preview=True
    )
    await callback.answer("ℹ️ Информация о компании")


@router.message(Command("help"))
async def help_command(
    message: Message,
    user: User
):
    """Handle /help command."""
    logger.info(f"User {user.telegram_id} requested help")
    
    help_text = (
        "❓ <b>Помощь по боту NOFACE.digital</b>\n\n"
        
        "🎯 <b>Основные функции:</b>\n"
        "• 🛠 <b>Заказать услугу</b> — оформить заявку на разработку\n"
        "• 👥 <b>Присоединиться к команде</b> — подать анкету для работы\n"
        "• 📞 <b>Связаться напрямую</b> — получить контакты\n"
        "• ℹ️ <b>О компании</b> — узнать больше о NOFACE.digital\n\n"
        
        "⚡ <b>Доступные команды:</b>\n"
        "• /start — главное меню\n"
        "• /help — эта справка\n"
        "• /contact — контактная информация\n\n"
        
        "🔄 <b>Как пользоваться:</b>\n"
        "1. Выберите нужное действие в главном меню\n"
        "2. Следуйте инструкциям бота\n"
        "3. Заполните необходимые формы\n"
        "4. Получите ответ от нашей команды\n\n"
        
        "💬 <b>Нужна дополнительная помощь?</b>\n"
        "Обращайтесь напрямую к CEO: @pavel_xdev"
    )
    
    await message.answer(
        help_text,
        reply_markup=get_main_menu(),
        parse_mode="HTML",
        disable_web_page_preview=True
    )


@router.message(Command("contact"))
async def contact_command(
    message: Message,
    user: User
):
    """Handle /contact command."""
    logger.info(f"User {user.telegram_id} requested contact info")
    
    contact_text = (
        "📞 <b>Контактная информация</b>\n\n"
        "🏢 <b>NOFACE.digital</b>\n"
        "Команда профессиональных разработчиков\n\n"
        
        "👨‍💼 <b>CEO:</b> @pavel_xdev\n"
        "💬 <b>Telegram:</b> @pavel_xdev\n"
        "🌐 <b>Веб-сайт:</b> https://noface.digital\n\n"
        
        "⚡ <b>Для быстрой связи:</b>\n"
        "Пишите напрямую CEO @pavel_xdev\n\n"
        
        "🕐 <b>Время ответа:</b> 2-4 часа\n"
        "🌍 <b>Режим работы:</b> 24/7, любая временная зона\n\n"
        
        "🚀 <b>Готовы обсудить ваш проект?</b>\n"
        "Используйте кнопки ниже для быстрого доступа!"
    )
    
    await message.answer(
        contact_text,
        reply_markup=get_main_menu(),
        parse_mode="HTML",
        disable_web_page_preview=True
    )


@router.message()
async def handle_text_messages(
    message: Message,
    user: User,
    state: FSMContext
):
    """Handle all text messages that don't match other handlers."""
    # Проверяем, не находится ли пользователь в состоянии заполнения формы
    current_state = await state.get_state()
    if current_state:
        # Если пользователь в любом состоянии FSM, не обрабатываем здесь
        return
    
    logger.info(f"User {user.telegram_id} sent unhandled message: {message.text}")
    
    # Ответ на любое текстовое сообщение
    response_text = (
        "💬 <b>Спасибо за сообщение!</b>\n\n"
        "🤖 Я бот для приема заявок на услуги и вакансии.\n\n"
        "💡 <b>Что вы можете сделать:</b>\n"
        "• 🛠 <b>Заказать услугу</b> — оформить заявку на разработку\n"
        "• 👥 <b>Присоединиться к команде</b> — подать анкету\n"
        "• 📞 <b>Связаться напрямую</b> — получить контакты CEO\n\n"
        "⚡ <b>Для личной консультации пишите напрямую:</b>\n"
        "👨‍💼 CEO: @pavel_xdev\n\n"
        "👇 <b>Выберите действие из меню:</b>"
    )
    
    await message.answer(
        response_text,
        reply_markup=get_main_menu(),
        parse_mode="HTML",
        disable_web_page_preview=True
    ) 